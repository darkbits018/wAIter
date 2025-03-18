import pandas as pd
from io import BytesIO
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app.models import MenuItem, User
from app.schemas import MenuItemCreate  # Define a Pydantic schema for validation

router = APIRouter()


### ✅ GET Menu Items for a Restaurant ###
@router.get("/{restaurant_id}")
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()


### ✅ SINGLE ITEM ADD API ###
@router.post("/")
def add_menu_item(
        item: MenuItemCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    # Ensure the user is an admin and has a restaurant
    if not current_user.is_admin or not current_user.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Add menu item for the admin's restaurant
    menu_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        image_url=item.image_url,
        category=item.category,
        is_veg=item.is_veg,
        restaurant_id=current_user.restaurant_id,
    )
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item


### ✅ BULK UPLOAD API ###
@router.post("/bulk-upload/")
async def bulk_upload_menu(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    # Ensure the user is an admin and has a restaurant
    if not current_user.is_admin or not current_user.restaurant_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Read file into DataFrame
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))  # For .xlsx files
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Check required columns
    required_columns = {"name", "description", "price", "image_url", "category", "is_veg", "meal_times"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail="Missing required columns in the file")

    # Process and insert data
    menu_items = []
    for _, row in df.iterrows():
        menu_item = MenuItem(
            name=row["name"],
            description=row["description"],
            price=row["price"],
            image_url=row["image_url"],
            category=row["category"],
            is_veg=row["is_veg"],
            restaurant_id=current_user.restaurant_id,
        )
        db.add(menu_item)
        db.commit()
        db.refresh(menu_item)
        menu_items.append(menu_item)

    return {"message": f"{len(menu_items)} menu items added successfully", "items": menu_items}
