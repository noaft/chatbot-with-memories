"This module defines the Settings class for managing application configuration using Pydantic. "
"The Settings class loads configuration values from environment variables, allowing for easy management of sensitive information such as API"

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    "Settings class for application configuration. This class uses Pydantic to load configuration values from environment variables. "

    LLM_url: str = Field(validation_alias='LLM_URL')  
    api_key: str = Field(alias='API_KEY')  
    model_name: str = Field(alias='MODEL_NAME')
    embed_model: str = Field(default='nomic-embed-text:latest', alias='EMBED_MODEL')
    embed_dims: int = Field(default=768, alias='EMBED_DIMS')