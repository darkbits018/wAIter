from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from firebase_admin import auth
from app.db import get_db
from app.models import User, Restaurant
import app.firebase  # Ensure Firebase is initialized
from routes.admin import router


# router = APIRouter()


@router.post("/login")
def login(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Authenticates user using Firebase ID token, then stores the user in PostgreSQL if not exists.
    """
    try:
        # Extract ID token from the Authorization header (Bearer <token>)
        id_token = authorization.split(" ")[1]

        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        phone_number = decoded_token.get("phone_number")

        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number not found in token")

        # Check if user already exists in PostgreSQL
        user = db.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            # Create new user in PostgreSQL
            new_user = User(phone_number=phone_number)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user

        # Fetch restaurant details if user is an admin
        restaurant = None
        if user.is_admin and user.restaurant_id:
            restaurant = db.query(Restaurant).filter(Restaurant.id == user.restaurant_id).first()

        return {
            "message": "Login successful",
            "user_id": user.id,
            "phone_number": user.phone_number,
            "role": "admin" if user.is_admin else "customer",
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name
            } if restaurant else None
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
