from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_TITLE: str = "Debit Maker"
    PROJECT_VERSION: str = "0.1.0"
    POSTGRES_USER : str =os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str=os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str=os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str=os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str=os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URL : str ="sqlite:///./sql_app.db"
  #  SQLALCHEMY_DATABASE_URL : str= f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SECRET_KEY:str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30 # 30 minutes
settings = Settings()   
    