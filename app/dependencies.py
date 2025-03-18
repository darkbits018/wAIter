import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, Header
import jwt
from firebase_admin import auth
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User, Restaurant

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        token = authorization.split(" ")[1]  # Extract Firebase token
        decoded_token = auth.verify_id_token(token)
        phone_number = decoded_token.get("phone_number")

        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def admin_required(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        token = authorization.split(" ")[1]  # Extract the token from "Bearer <token>"
        decoded_token = auth.verify_id_token(token)
        phone_number = decoded_token.get("phone_number")

        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")

        restaurant = db.query(Restaurant).filter(Restaurant.id == user.restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=403, detail="Restaurant not found")

        return user  # This user object now includes the `restaurant_id`

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")


def auth_required(authorization: str = Header(...), db: Session = Depends(get_db)):
    """ Middleware to authenticate any user (customer or admin) """
    try:
        token = authorization.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        phone_number = decoded_token.get("phone_number")

        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user  # Returns the user object
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
