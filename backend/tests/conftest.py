import pytest
from app import app as flask_app
import mongomock

@pytest.fixture(scope="session")
def test_client():
    # Flask provides a way to test our application by exposing the Werkzeug test Client.
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def use_mongomock(monkeypatch):
    """
    Patch MongoClient to use mongomock for all tests,
    ensuring all tests use in-memory MongoDB.
    """
    monkeypatch.setattr('app.models.MongoClient', mongomock.MongoClient)
