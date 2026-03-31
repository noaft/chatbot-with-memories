# Configuration Module ⚙️
This folder manages all system-wide settings, environment variables, and static parameters.

### Key Components:
- **`settings.py`**: Responsible for loading environment variables (API Keys, Database URLs) from the `.env` file.
- **Model Parameters**: Defines LLM configurations such as `temperature`, `max_tokens`, and `model_name`.
- **Database Config**: Connection strings and settings for the Vector Store (e.g., Qdrant or ChromaDB).

### Security Note:
- Never hardcode sensitive API keys here. Always use the `.env` file and keep it excluded from version control (git).