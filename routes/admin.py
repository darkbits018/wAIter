from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Restaurant, User, MenuItem, Order, Table
from app.dependencies import admin_required
from app.schemas import RestaurantCreate, AdminCreate, MenuItemCreate

router = APIRouter()


# ✅ Register a new restaurant
@router.post("/register_restaurant")
def register_restaurant(
        restaurant_data: RestaurantCreate,  # Receive JSON body instead of query params
        db: Session = Depends(get_db)
):
    existing_restaurant = db.query(Restaurant).filter(Restaurant.name == restaurant_data.name).first()
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant already exists")

    new_restaurant = Restaurant(name=restaurant_data.name)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return {"message": "Restaurant registered successfully", "restaurant_id": new_restaurant.id}


# Register a new admin
@router.post("/register_admin")
def register_admin(
        admin_data: AdminCreate,  # Accept JSON request body
        db: Session = Depends(get_db)
):
    # Check if the restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == admin_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Check if user exists
    user = db.query(User).filter(User.phone_number == admin_data.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Ask them to log in first.")

    # Update user role to admin
    user.is_admin = True
    user.restaurant_id = admin_data.restaurant_id  # Link admin to the restaurant
    db.commit()

    return {"message": "Admin registered successfully", "admin_id": user.id, "restaurant_id": user.restaurant_id}


#
# @router.post("/menu/")
# def add_menu_item(item: MenuItemCreate, user=Depends(admin_required), db: Session = Depends(get_db)):
#     restaurant_id = user.restaurant_id  # Get the restaurant ID from the logged-in admin
#     new_item = MenuItem(name=item.name, price=item.price, description=item.description, image_url=item.image_url,
#                         restaurant_id=restaurant_id)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item


# ✅ Admin can view their restaurant details
@router.get("/restaurant/")
def get_restaurant(user=Depends(admin_required), db: Session = Depends(get_db)):
    if not user.restaurant_id:
        raise HTTPException(status_code=400, detail="Admin is not linked to any restaurant")

    restaurant = db.query(Restaurant).filter(Restaurant.id == user.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return {"restaurant_id": restaurant.id, "name": restaurant.name}


router = APIRouter()


# Helper function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# ✅ Create tables and generate QR codes
@router.post("/tables/")
def create_tables(
        restaurant_id: int,
        number_of_tables: int,
        user=Depends(admin_required),
        db: Session = Depends(get_db),
):
    # Ensure the admin has access to the restaurant
    if user.restaurant_id != restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Create tables and generate QR codes
    tables = []
    for table_number in range(1, number_of_tables + 1):
        qr_data = f"https://api.waiter.com/customer/qr/{restaurant_id}/{table_number}"
        qr_code_url = generate_qr_code(qr_data)

        new_table = Table(
            table_number=table_number,
            restaurant_id=restaurant_id,
            qr_code_url=qr_code_url,
        )
        db.add(new_table)
        db.commit()
        db.refresh(new_table)
        tables.append(new_table)

    return {
        "message": "Tables created successfully",
        "tables": [
            {
                "table_number": table.table_number,
                "qr_code_url": table.qr_code_url,
            }
            for table in tables
        ],
    }


# ✅ Fetch all tables for a restaurant
@router.get("/tables/{restaurant_id}")
def get_tables(
        restaurant_id: int,
        user=Depends(admin_required),
        db: Session = Depends(get_db),
):
    # Ensure the admin has access to the restaurant
    if user.restaurant_id != restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    tables = db.query(Table).filter(Table.restaurant_id == restaurant_id).all()
    return [
        {
            "table_number": table.table_number,
            "qr_code_url": table.qr_code_url,
        }
        for table in tables
    ]
