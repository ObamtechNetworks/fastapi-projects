from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = ConfigDict(env_file=".env")

# create an instance of the Settings class to load the environment variables from the .env file. This instance will be used to access the configuration settings throughout the application.
settings = Settings()
