from fastapi import FastAPI
import uvicorn

from app.auth import router as auth_router
from app.menu import router as menu_router
from app.orders import router as orders_router
from routes.admin import router as admin_router  # ✅ Import admin router

app = FastAPI(title="AI Waiter Backend")

# Include API routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(menu_router, prefix="/menu", tags=["Menu"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])  # ✅ Register admin routes

@app.get("/")
def home():
    return {"message": "Welcome to AI Waiter Backend"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)