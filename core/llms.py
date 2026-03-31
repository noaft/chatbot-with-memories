from typing import List, Union
import openai
from openai.types.chat import (
    ChatCompletionSystemMessageParam, 
    ChatCompletionUserMessageParam, 
)

class LLM:
    """
    LLM class for interacting with a language model API. 
    This class initializes the OpenAI client and provides a method to generate responses based on system prompts and user input. 
    """
    def __init__(self, model_name: str, api_key: str = None, llm_url: str = None):
        self.api_key = api_key  
        self.llm_url = llm_url or "http://localhost:11434/v1"
        self.model_name = model_name

        self.client = openai.OpenAI(
            api_key=self.api_key, 
            base_url=self.llm_url
        )

    def generate(self, prompt: str, user_input: str) -> str:
        """
        Send system prompt and user input to receive a response.
        """
        messages: List[Union[ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam]] = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7
            )
            return chat_completion.choices[0].message.content
        
        except Exception as e:
            return f"Error callings LLM: {str(e)}"

# --- Example usage ---
if __name__ == "__main__":
    llm = LLM(model_name="qwen2.5:1.7b") 
    
    system_prompt = "Bạn là một chuyên gia về AI, hãy trả lời ngắn gọn."
    user_query = "Ollama là gì?"
    
    result = llm.generate(system_prompt, user_query)
    print(f"Robot: {result}")