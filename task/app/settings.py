from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@maprac6-rabbitmq-1:5672"
    postgres_url: str = "postgresql://postgres:potemkin@172.17.0.1:5432/test"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
