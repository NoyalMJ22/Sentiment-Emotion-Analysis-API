from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Sentiment & Emotion Analysis API"
    APP_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Model settings
    SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    EMOTION_MODEL: str = "j-hartmann/emotion-english-distilroberta-base"
    
    # Security
    API_KEY: str = "secret-super-key-123"
    
    # Scalability
    REDIS_URL: str = "redis://localhost:6379"
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
