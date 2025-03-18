import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import auth, credentials

# Load environment variables from .env file
load_dotenv()

# Get the path to the Firebase credentials from the environment variable
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

# Load Firebase Admin SDK credentials
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)