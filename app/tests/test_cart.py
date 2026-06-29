from app.tests.helpers import add_keyboard


# Verify duplicate products are merged and subtotal is updated.
def test_cart_merge(api_client):

    add_keyboard(api_client, 2)
    add_keyboard(api_client, 3)

    response = api_client.get("/cart")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 5
    assert data["subtotal"] == 5000


# Verify cart correctly handles large quantity orders.
def test_large_order(api_client):

    api_client.post(
        "/cart/items",
        json={
            "product_id": 99,
            "name": "Monitor",
            "price": 20000,
            "quantity": 10,
        },
    )

    response = api_client.get("/cart")

    assert response.status_code == 200

    data = response.json()

    assert data["subtotal"] == 200000

    # Verify adding the same product twice with different prices keeps the original price.
def test_same_product_different_price_keeps_original(api_client):
    api_client.post("/cart/items", json={
        "product_id": 1, "name": "Keyboard", "price": 1000, "quantity": 1
    })
    api_client.post("/cart/items", json={
        "product_id": 1, "name": "Keyboard", "price": 1500, "quantity": 1
    })

    response = api_client.get("/cart")
    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["price"] == 1000
    assert data["subtotal"] == 2000