from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from app.db import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, default="customer")
    is_admin = Column(Boolean, default=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=True)  # Link admin to restaurant

    restaurant = relationship("Restaurant")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String)
    category = Column(String, nullable=False)  # Single category per item
    is_veg = Column(String, nullable=False)  # "veg", "non-veg", or "contains-egg"
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    restaurant = relationship("Restaurant")
    meal_times = relationship("MenuItemMealTime", back_populates="menu_item")


class MenuItemMealTime(Base):
    __tablename__ = "menu_item_meal_times"
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    meal_time = Column(String, nullable=False)  # Values: "breakfast", "lunch", "dinner", "all-day"

    menu_item = relationship("MenuItem", back_populates="meal_times")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)
    table_number = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))  # Link to restaurant

    user = relationship("User")
    item = relationship("MenuItem")
    restaurant = relationship("Restaurant")

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    qr_code_url = Column(String, nullable=False)  # URL to the QR code image

    restaurant = relationship("Restaurant")