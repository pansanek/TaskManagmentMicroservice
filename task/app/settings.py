from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    amqp_url: str
    postgres_url: str 
    port: int

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
