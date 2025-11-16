from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMSettings(BaseSettings):
    OPENROUTER_API_KEY: str | None = None
    OPENAI_MODEL: str = "mistral-nemo"
    OPENROUTER_URL: str = "https://openrouter.ai/api/v1/chat/completions"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,   # <-- accept lowercase keys
    )

settings = LLMSettings()
