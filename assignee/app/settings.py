from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@maprac6-rabbitmq-1:5672"

settings = Settings()