from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str

class AdminCreate(BaseModel):
    phone_number: str
    restaurant_id: int

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    category: str  # "Appetizers", "Drinks", etc.
    is_veg: str  # "veg", "non-veg", "contains-egg"