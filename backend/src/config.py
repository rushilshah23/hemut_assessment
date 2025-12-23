from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URL = os.environ['DATABASE_URL']

    JWT_SECRET_KEY = "super-secret-change-this"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
