import pytest
from app.utils import create_token

@pytest.fixture
def authed_headers():
    # Simulate a user for endpoints requiring login
    token = create_token("user123", "user")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def provider_headers():
    token = create_token("prov123", "provider")
    return {"Authorization": f"Bearer {token}"}

def test_health(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Healthy" in resp.json["message"]

def test_subscription_flow(client, authed_headers):
    # POST create subscription
    resp = client.post("/subscriptions/", json={
        "provider_id": "prov-test",
        "payment_id": "pay-test",
        "plan_type": "monthly",
        "amount": 100.0
    }, headers=authed_headers)
    assert resp.status_code == 201

    # GET list
    resp2 = client.get("/subscriptions/", headers=authed_headers)
    assert resp2.status_code == 200
    assert isinstance(resp2.json, list)

def test_booking_flow(client, authed_headers):
    # Create a provider and schedule first
    schedule_resp = client.post("/schedules/", headers={"Authorization": create_token("prov777", "provider")},
        json={
        "route": "Test Route",
        "provider_id": "prov777",
        "timings": ["08:00"],
        "days": ["Mon"],
        "seats": 10,
        "available_seats": 10,
        "is_active": True
    })
    assert schedule_resp.status_code == 201

    # Insert a schedule for booking (simulate what the POST does)
    from app.models import get_db
    db = get_db()
    sched = db.schedules.find_one({"provider_id": "prov777"})
    schedule_id = str(sched["_id"])
    # Book a seat
    resp = client.post("/bookings/", json={
        "schedule_id": schedule_id,
        "date": "2024-06-11",
        "time": "08:00"
    }, headers=authed_headers)
    assert resp.status_code == 201
    assert "Booking successful" in resp.json["message"]

    # Cancel booking test
    booking_obj = db.bookings.find_one({"user_id": "user123"})
    booking_id = str(booking_obj["_id"])
    resp = client.post(f"/bookings/{booking_id}/cancel", headers=authed_headers)
    assert resp.status_code == 200

def test_notification_flow(client, authed_headers):
    # Post notification
    resp = client.post("/notifications/", json={
        "message": "Your trip at 08:00 AM",
        "notif_type": "reminder"
    }, headers=authed_headers)
    assert resp.status_code == 201

    # List notifications
    resp2 = client.get("/notifications/", headers=authed_headers)
    assert resp2.status_code == 200
    assert isinstance(resp2.json, list)

    db = __import__("app.models", fromlist=["get_db"]).get_db()
    obj = db.notifications.find_one({"user_id": "user123"})
    notif_id = str(obj["_id"])
    # Mark read
    resp = client.post(f"/notifications/{notif_id}/mark_read", headers=authed_headers)
    assert resp.status_code == 200

def test_payment_flow(client, authed_headers):
    # Insert for payment
    resp = client.post("/payments/", json={
        "provider_id": "prov888",
        "amount": 500.0,
        "subscription_id": "sub-x"
    }, headers=authed_headers)
    assert resp.status_code == 201
    assert "Payment successful" in resp.json["message"]
    # List payments
    resp2 = client.get("/payments/", headers=authed_headers)
    assert resp2.status_code == 200

def test_profile_get_and_edit(client, authed_headers):
    from app.models import get_db
    db = get_db()
    # Insert user into DB for GET/PUT test (simulate signup effect)
    db.users.insert_one({
        "_id": "user123",
        "email": "profile@example.com",
        "password": "hash",
        "name": "Myself",
        "phone": "9723445234",
        "user_type": "user"
    })
    # GET profile
    resp = client.get("/profile/", headers=authed_headers)
    assert resp.status_code == 200
    assert "email" in resp.json
    # PUT profile
    resp2 = client.put("/profile/", headers=authed_headers, json={"name": "Updated Name"})
    assert resp2.status_code == 200
    # Test for provider too
    db.providers.insert_one({
        "_id": "prov123",
        "email": "prov@example.com",
        "password": "hash",
        "provider_name": "Provider",
        "phone": "9992334455",
        "user_type": "provider"
    })
    resp3 = client.get("/profile/", headers={"Authorization": f"Bearer {create_token('prov123', 'provider')}"})
    assert resp3.status_code == 200
