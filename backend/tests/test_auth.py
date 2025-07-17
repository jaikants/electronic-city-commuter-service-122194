import pytest

@pytest.fixture
def client(test_client):
    return test_client

def test_user_signup_and_duplicate(client):
    resp = client.post("/auth/signup/user", json={
        "email": "user1@example.com",
        "password": "pw1",
        "name": "User One",
        "phone": "9991234567"
    })
    assert resp.status_code == 201
    assert "Signup successful" in resp.json["message"]

    # Duplicate signup
    resp2 = client.post("/auth/signup/user", json={
        "email": "user1@example.com",
        "password": "pw1",
        "name": "User One",
        "phone": "9991234567"
    })
    assert resp2.status_code == 409

def test_provider_signup_and_duplicate(client):
    resp = client.post("/auth/signup/provider", json={
        "email": "prov1@example.com",
        "password": "provpass",
        "provider_name": "ETrans Co",
        "phone": "9981234567"
    })
    assert resp.status_code == 201

    # Duplicate
    resp2 = client.post("/auth/signup/provider", json={
        "email": "prov1@example.com",
        "password": "provpass",
        "provider_name": "ETrans Co",
        "phone": "9981234567"
    })
    assert resp2.status_code == 409

def test_login_success_and_invalid(client):
    # First sign up user
    client.post("/auth/signup/user", json={
        "email": "user2@example.com",
        "password": "pw2",
        "name": "User Two",
        "phone": "9876543211"
    })
    # Success
    resp = client.post("/auth/login", json={
        "email": "user2@example.com",
        "password": "pw2"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json

    # Bad login
    resp2 = client.post("/auth/login", json={
        "email": "user2@example.com",
        "password": "wrong"
    })
    assert resp2.status_code == 401
