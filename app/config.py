import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
SECRET_KEY = os.getenv("SECRET_KEY", "b332c8f78fd6e59cafff8430883a9d13958997d219b6dbb8aa8c3a4160a83273")  # Change this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiry time (optional)
