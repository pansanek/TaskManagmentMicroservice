from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@51.250.26.59:5672"
    postgres_url: str = "postgresql://postgres:Alex2002@localhost:5432/test"

settings = Settings()