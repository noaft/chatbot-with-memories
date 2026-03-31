chainlit run main.py -w 
# Chatbot with Memories

This project is a simple chatbot designed to demonstrate how to implement both long-term and short-term memory in conversational AI. It is intended for learning and experimentation with memory management in chatbots.

## Features

- **Short-term memory**: Remembers the recent context of the conversation, allowing the chatbot to respond coherently within a session.
- **Long-term memory**: Stores important information from past conversations, enabling the chatbot to recall facts or user preferences across sessions.
- Simple and easy-to-understand codebase for educational purposes.
- Extensible for more advanced memory or AI features.

## Project Goals

- Learn how to build a chatbot with memory capabilities.
- Understand the difference between short-term and long-term memory in conversational systems.
- Provide a foundation for experimenting with memory-augmented chatbots.

## How It Works

1. **Short-term memory** is typically implemented as a context window, storing the last N messages or turns in the conversation.
2. **Long-term memory** is implemented as a persistent storage (e.g., file, database, or vector store) that saves key information or facts extracted from conversations.
3. The chatbot uses both memories to generate more relevant and context-aware responses.

## Usage

1. Clone this repository.
2. Install dependencies (see `pyproject.toml`).
3. Run the chatbot using:
	```bash
	uv run main.py
	```
4. Interact with the chatbot and observe how it remembers information within and across sessions.

## Future Improvements

- Add support for more advanced memory retrieval (e.g., semantic search).
- Integrate with external knowledge bases.
- Improve conversation quality with advanced language models.

## License

MIT License
