from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Order, User, Restaurant
from app.dependencies import get_current_user, auth_required

router = APIRouter()

@router.get("/{restaurant_id}/{table_number}")
def get_orders_by_table(restaurant_id: int, table_number: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.restaurant_id == restaurant_id, Order.table_number == table_number).all()

@router.post("/")
def place_order(item_id: int, quantity: int, table_number: int, user=Depends(auth_required), db: Session = Depends(get_db)):
    """
    Place an order using the restaurant_id from the table QR code.
    """
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Fetch restaurant_id based on table number
    restaurant_id = db.query(Restaurant).filter(Restaurant.tables.any(table_number=table_number)).first()

    if not restaurant_id:
        raise HTTPException(status_code=400, detail="Invalid table number")

    order = Order(user_id=user.id, item_id=item_id, quantity=quantity, table_number=table_number, restaurant_id=restaurant_id.id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"message": "Order placed successfully", "order_id": order.id}

