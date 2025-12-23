from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URL = os.environ['DATABASE_URL']