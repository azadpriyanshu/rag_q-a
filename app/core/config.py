from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GOOGLE_API_KEY: str
    LLM_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    SIMILARITY_THRESHOLD: float = 0.75
    MAX_CONTEXT_CHARS: int = 12000

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()