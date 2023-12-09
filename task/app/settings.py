from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@maprac6-rabbitmq-1:5672"
    postgres_url: str = "postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/tasks"
    port: int = 80

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()