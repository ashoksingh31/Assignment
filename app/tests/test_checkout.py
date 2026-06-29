from app.tests.helpers import add_keyboard


# Verify successful checkout without applying any discount.
def test_checkout_without_discount(api_client):

    add_keyboard(api_client, 5)

    response = api_client.post("/checkout", json={})

    assert response.status_code == 200

    data = response.json()

    assert data["subtotal"] == 5000
    assert data["discount"] == 0
    assert data["total"] == 5000


# Verify coupon generation after every third successful order.
def test_discount_generation_after_third_order(api_client):

    for _ in range(3):
        add_keyboard(api_client, 1)
        api_client.post("/checkout", json={})

    response = api_client.post("/admin/discount/generate")

    assert response.status_code == 200

    data = response.json()

    assert data["percentage"] == 10
    assert data["code"] != ""


# Verify valid discount code is applied during checkout.
def test_checkout_with_discount(api_client):

    for _ in range(3):
        add_keyboard(api_client, 1)
        api_client.post("/checkout", json={})

    coupon = api_client.post(
        "/admin/discount/generate"
    ).json()["code"]

    add_keyboard(api_client, 5)

    response = api_client.post(
        "/checkout",
        json={
            "discount_code": coupon
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subtotal"] == 5000
    assert data["discount"] == 500
    assert data["total"] == 4500


# Verify invalid discount codes are rejected.
def test_invalid_discount(api_client):

    add_keyboard(api_client, 5)

    response = api_client.post(
        "/checkout",
        json={
            "discount_code": "INVALID123"
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Invalid discount code"


# Verify checkout fails when the cart is empty.
def test_empty_cart_checkout(api_client):

    response = api_client.post("/checkout", json={})

    assert response.status_code == 400

    assert response.json()["detail"] == "Cart is empty"

    # Verify a discount code cannot be reused after it has been applied once.
def test_discount_code_reuse(api_client):
    for _ in range(3):
        add_keyboard(api_client, 1)
        api_client.post("/checkout", json={})

    coupon = api_client.post("/admin/discount/generate").json()["code"]

    add_keyboard(api_client, 5)
    api_client.post("/checkout", json={"discount_code": coupon})

    add_keyboard(api_client, 5)
    response = api_client.post("/checkout", json={"discount_code": coupon})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid discount code"


# Verify cart is empty after a successful checkout.
def test_cart_cleared_after_checkout(api_client):
    add_keyboard(api_client, 3)
    api_client.post("/checkout", json={})

    response = api_client.get("/cart")
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["subtotal"] == 0


# Verify total_discount_given in stats is updated correctly after a discounted order.
def test_stats_discount_given(api_client):
    for _ in range(3):
        add_keyboard(api_client, 1)
        api_client.post("/checkout", json={})

    coupon = api_client.post("/admin/discount/generate").json()["code"]

    add_keyboard(api_client, 5)
    api_client.post("/checkout", json={"discount_code": coupon})

    response = api_client.get("/admin/stats")
    assert response.json()["total_discount_given"] == 500