from typing import Annotated
import openai
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from mem0 import Memory


class State(TypedDict):
    messages: Annotated[list, add_messages]
    system_prompt: str


class LLM:
    """
    LLM class with short-term memory (LangGraph MemorySaver per session)
    and long-term memory (mem0 across sessions).
    """
    def __init__(self, model_name: str, api_key: str = None, llm_url: str = None, embed_model: str = "nomic-embed-text:latest", embed_dims: int = 768):
        self.api_key = api_key
        self.llm_url = llm_url or "http://localhost:11434/v1"
        self.model_name = model_name

        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.llm_url
        )

        # Short-term memory: per-session conversation history
        self.memory = MemorySaver()
        self.graph = self._build_graph()

        # Long-term memory: persists facts across sessions via mem0
        mem_config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": model_name,
                    "openai_base_url": self.llm_url,
                    "api_key": self.api_key,
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": embed_model,
                    "openai_base_url": self.llm_url,
                    "api_key": self.api_key,
                    "embedding_dims": embed_dims,
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "embedding_model_dims": embed_dims,
                }
            },
        }

        print(f"Initializing long-term memory with config: {mem_config}")
        self.long_term_memory = Memory.from_config(mem_config)

    def _call_llm(self, state: State) -> dict:
        role_map = {"human": "user", "ai": "assistant", "system": "system"}
        openai_messages = [{"role": "system", "content": state["system_prompt"]}]
        for m in state["messages"]:
            role = role_map.get(m.type, "user")
            openai_messages.append({"role": role, "content": m.content})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=openai_messages,
            temperature=0.7
        )
        return {"messages": [{"role": "assistant", "content": response.choices[0].message.content}]}

    def _build_graph(self):
        graph = StateGraph(State)
        graph.add_node("llm", self._call_llm)
        graph.add_edge(START, "llm")
        graph.add_edge("llm", END)
        return graph.compile(checkpointer=self.memory)

    def generate(self, prompt: str, user_input: str, thread_id: str = "default", user_id: str = "default_user") -> str:
        """
        Generate a response with short-term (LangGraph) and long-term (mem0) memory.
        Relevant long-term memories are injected into the system prompt each turn,
        and the interaction is saved to mem0 after responding.
        """
        # Retrieve relevant long-term memories for this user
        past_memories = self.long_term_memory.search(user_input, user_id=user_id)
        memory_facts = "\n".join(
            f"- {m['memory']}" for m in past_memories.get("results", [])
        )

        augmented_prompt = prompt
        if memory_facts:
            augmented_prompt = f"{prompt}\n\nRelevant long-term memories about the user:\n{memory_facts}"

        config = {"configurable": {"thread_id": thread_id}}
        try:
            result = self.graph.invoke(
                {"messages": [{"role": "user", "content": user_input}], "system_prompt": augmented_prompt},
                config=config
            )
            response_text = result["messages"][-1].content

            # Persist this turn to long-term memory
            self.long_term_memory.add(
                [
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": response_text},
                ],
                user_id=user_id,
            )

            return response_text
        except Exception as e:
            return f"Error calling LLM: {str(e)}"


# --- Example usage ---
if __name__ == "__main__":
    llm = LLM(model_name="qwen2.5:1.7b")

    system_prompt = "Bạn là một chuyên gia về AI, hãy trả lời ngắn gọn."

    print("Robot:", llm.generate(system_prompt, "Ollama là gì?", thread_id="test", user_id="alice"))
    print("Robot:", llm.generate(system_prompt, "Nó có ưu điểm gì?", thread_id="test", user_id="alice"))

