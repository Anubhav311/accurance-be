from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    origin_localhost: str = os.getenv("ORIGIN_HOST")
    origin_localhost_2: str = os.getenv("ORIGIN_HOST_2")

settings = Settings()