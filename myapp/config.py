from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True
    SERVER_NAME = "https://futurebank.local"
    PREFERRED_URL_SCHEME = 'https'
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True