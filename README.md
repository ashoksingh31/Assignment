# Ecommerce Store API

A simple ecommerce backend built using **FastAPI** that allows customers to add items to a shopping cart, checkout orders, and apply discount coupons. The application also provides admin APIs to generate discount codes and view store statistics.

The project uses **in-memory storage**, so no database setup is required.

---

# Features

- Add items to cart
- View cart and subtotal
- Checkout with or without discount codes
- Single-use discount coupons
- Generate coupons after every nth order
- View all orders
- View generated discount codes
- View store statistics
- Unit tests using Pytest
- Swagger API documentation

---

# Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

# Project Structure

```
assignment/
│
├── app/
│   ├── routes/
│   │   ├── admin.py
│   │   ├── cart.py
│   │   └── checkout.py
│   │
│   ├── services/
│   │   ├── cart_service.py
│   │   ├── checkout_service.py
│   │   └── discount_service.py
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── helpers.py
│   │   ├── test_admin.py
│   │   ├── test_cart.py
│   │   └── test_checkout.py
│   │
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── storage.py
│
├── README.md
├── DECISIONS.md
├── requirements.txt
└── .gitignore
```

---

# API Endpoints

## Cart

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/cart/items` | Add an item to cart |
| GET | `/cart` | View cart and subtotal |

---

## Checkout

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/checkout` | Place an order with an optional discount code |

---

## Admin

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/admin/discount/generate` | Generate a discount coupon when eligible |
| GET | `/admin/orders` | View all orders |
| GET | `/admin/discounts` | View generated discount codes |
| GET | `/admin/stats` | View store statistics |

---

# Running the Project

## 1. Clone the repository

```bash
git clone <repository-url>
cd assignment
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the application

```bash
uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Running Tests

Execute all unit tests using:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

---

# Assumptions

- Inventory is assumed to be unlimited.
- Discount coupons are valid for a single use.
- All data is stored in memory.
- No authentication is implemented for admin APIs.
- Coupons are generated only when the configured order threshold is reached.

---

# Design Decisions

Key design decisions and trade-offs are documented in **DECISIONS.md**.

---

# Future Improvements

If this project were extended further, the following improvements could be made:

- Database integration (PostgreSQL/MySQL)
- JWT authentication for admin endpoints
- Inventory management
- Product catalog APIs
- Coupon expiration and configurable discount rules
- Docker support
- CI/CD pipeline
- Logging and monitoring

---

# API Testing

The project includes automated tests covering:

- Cart operations
- Checkout flow
- Discount generation
- Coupon validation
- Empty cart handling
- Invalid coupon handling
- Admin statistics
- Orders listing
- Discount listing
- Large order scenarios

---

# Author

**Ashok Kumar Singh**