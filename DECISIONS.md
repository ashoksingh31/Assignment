# Design Decisions

## Decision: Use In-Memory Storage

**Context:** The application needs to store cart items, orders, discount codes, and store statistics.

**Options Considered:**
- Option A: Use an in-memory store with Python objects.
- Option B: Use a relational database such as SQLite or PostgreSQL.

**Choice:** In-memory storage.

**Why:** The assignment explicitly mentioned that a database was not required. Using in-memory storage kept the project lightweight and allowed me to focus on implementing the business logic instead of database configuration. Since the storage logic is isolated, replacing it with a database later would require minimal changes.

---

## Decision: Keep Business Logic Separate from Routes

**Context:** The APIs contain logic for cart operations, checkout, discount validation, and statistics.

**Options Considered:**
- Option A: Write all logic directly inside the route handlers.
- Option B: Move business logic into dedicated service modules.

**Choice:** Separate service layer.

**Why:** I wanted the routes to only deal with requests and responses while keeping all business rules in one place. This also made the code easier to test and prevented duplication across different endpoints.

---

## Decision: Generate Discount Codes Through an Admin API

**Context:** The system needs to generate a discount code after every nth completed order.

**Options Considered:**
- Option A: Automatically generate the coupon during checkout.
- Option B: Expose an admin endpoint that generates the coupon only when the condition is met.

**Choice:** Admin endpoint.

**Why:** Separating coupon generation from checkout keeps the checkout flow simple and gives the admin explicit control over when coupons are created. It also avoids generating duplicate coupons accidentally.

---

## Decision: Single-Use Discount Codes

**Context:** A customer should not be able to reuse the same coupon multiple times.

**Options Considered:**
- Option A: Allow coupons to be reused.
- Option B: Mark coupons as used after a successful checkout.

**Choice:** Single-use coupons.

**Why:** One-time coupons are simple to implement and prevent repeated use of the same discount. A boolean flag was sufficient for the current requirements without adding unnecessary complexity.

---

## Decision: Use Pydantic Schemas for API Validation

**Context:** Incoming requests and outgoing responses need validation and documentation.

**Options Considered:**
- Option A: Validate data manually.
- Option B: Use Pydantic models.

**Choice:** Pydantic schemas.

**Why:** FastAPI integrates naturally with Pydantic, making request validation automatic while also generating Swagger documentation without additional effort.

---

## Decision: Assume Unlimited Inventory

**Context:** The cart allows customers to add products before checkout.

**Options Considered:**
- Option A: Implement stock management.
- Option B: Assume products are always available.

**Choice:** Unlimited inventory.

**Why:** Inventory management was outside the scope of the assignment. Implementing stock tracking would require additional models and business rules that weren't necessary for demonstrating the required functionality.

---

## Decision: Organize Tests by Feature

**Context:** The project includes tests for cart operations, checkout, and admin functionality.

**Options Considered:**
- Option A: Keep all tests in a single file.
- Option B: Split tests into separate modules based on functionality.

**Choice:** Separate test files.

**Why:** Keeping tests grouped by feature makes them easier to understand and maintain. Shared setup code was moved to `conftest.py`, and common helper functions were placed in `helpers.py` to avoid duplication.

---

## Decision: No Authentication for Admin APIs

**Context:** The admin endpoints expose statistics, discount generation, and order details.

**Options Considered:**
- Option A: Add authentication and authorization.
- Option B: Leave the endpoints open.

**Choice:** No authentication.

**Why:** Authentication wasn't part of the assignment requirements. If this project were extended further, these endpoints would be protected using JWT authentication and role-based access control.