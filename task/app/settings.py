from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    amqp_url: str
    postgres_url: str 
    port: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
