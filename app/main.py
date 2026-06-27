from fastapi import FastAPI

from app.routes.cart import router as cart_router
from app.routes.checkout import router as checkout_router
from app.routes.admin import router as admin_router

app = FastAPI(
    title="E-Commerce Store API",
    version="1.0.0"
)

app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(checkout_router, tags=["Checkout"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root():
    return {
        "message": "API is running"
    }