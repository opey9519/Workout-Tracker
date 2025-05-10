import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()  # Load environment variables from .env file

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "your_secure_password"))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "my_fitness_app")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SQLALCHEMY_DATABASE_URI = DATABASE_URL

# Disables Flask-SQLAlchemy event tracking for performance
SQLALCHEMY_TRACK_MODIFICATIONS = False
