from fastapi import FastAPI

from app.routes.cart import router as cart_router
from app.routes.checkout import router as checkout_router
from app.routes.admin import router as admin_router


# ---------------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------------
# Initialises the FastAPI app and registers all route groups.
# Business logic lives in services/, HTTP concerns live in routes/.
# ---------------------------------------------------------------------------

app = FastAPI(
    title="E-Commerce Store API",
    version="1.0.0",
)

# Cart endpoints — add items, view cart
app.include_router(cart_router, prefix="/cart", tags=["Cart"])

# Checkout endpoint — place orders with optional discount
app.include_router(checkout_router, prefix="/checkout", tags=["Checkout"])

# Admin endpoints — stats, orders, discount code generation
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root():
    """Health check — confirms the API is running."""
    return {"message": "API is running"}