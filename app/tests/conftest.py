import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import cart, orders, discount_codes, stats


# ---------------------------------------------------------------------------
# Test Configuration
# ---------------------------------------------------------------------------
# This file is auto-loaded by pytest before any test runs.
# It provides shared fixtures available to all test files.
# ---------------------------------------------------------------------------


@pytest.fixture
def api_client():
    """
    Provide a fresh TestClient for each test.
    TestClient wraps the FastAPI app and allows HTTP calls without
    spinning up a real server.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    """
    Reset all in-memory storage before every test automatically.

    `autouse=True` means this runs for every test without needing to
    explicitly request it. This prevents state from one test bleeding
    into the next — e.g. a checkout in test A should not affect order
    counts seen by test B.
    """
    cart.clear()
    orders.clear()
    discount_codes.clear()

    stats.total_orders = 0
    stats.total_items_sold = 0
    stats.total_revenue = 0
    stats.total_discount_given = 0
    stats.discount_codes_generated = 0
    stats.discount_codes_used = 0
    stats.last_discount_order = 0