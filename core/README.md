# Core Module 🧠
This directory contains the central logic of the chatbot, including AI orchestration and memory management.

### Key Components:
- **`engine.py`**: Handles interactions with the Large Language Model (LLM). This is where prompts are constructed and model responses are processed.
- **`memory_mgr.py`**: Manages long-term memory using **Mem0**. It is responsible for storing, searching, and updating user context within the Vector Database.

### Execution Flow:
1. Receive user input from the UI.
2. Query `memory_mgr` to retrieve relevant past user information.
3. Inject context into the System Prompt and send it to the LLM via `engine`.
4. Return the response to the user and asynchronously update the memory.