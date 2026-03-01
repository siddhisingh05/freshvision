"""
tests/test_routes.py — Basic route tests
Run: pytest tests/
"""
import pytest
from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE"] = ":memory:"   # use in-memory DB for tests
    with app.test_client() as c:
        yield c


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_predict_page_get(client):
    resp = client.get("/predict")
    assert resp.status_code == 200


def test_history_page(client):
    resp = client.get("/history")
    assert resp.status_code == 200


def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
