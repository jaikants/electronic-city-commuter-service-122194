import pytest
from app.models import (
    UserSchema, ProviderSchema, SubscriptionSchema, ScheduleSchema,
    BookingSchema, NotificationSchema, PaymentSchema
)
from marshmallow import ValidationError

# Sample data dicts for each schema
def valid_user():
    return {
        "email": "john@example.com",
        "password": "pass1234",
        "name": "John Doe",
        "phone": "9876543210",
        "profile_picture": None,
        "user_type": "user"
    }

def valid_provider():
    return {
        "email": "prov@example.com",
        "password": "provpass",
        "provider_name": "EC Trans",
        "phone": "9443222222",
        "user_type": "provider"
    }

def valid_subscription():
    return {
        "user_id": "507f1f77bcf86cd799439011",
        "provider_id": "507f1f77bcf86cd799439012",
        "start_date": "2024-06-10",
        "end_date": "2024-07-10",
        "plan_type": "monthly",
        "amount": 1200.0,
        "payment_id": "payid123",
        "is_active": True
    }

def valid_schedule():
    return {
        "provider_id": "abc-provider",
        "route": "ECity-ITPL",
        "timings": ["08:00", "09:30"],
        "days": ["Mon", "Tue"],
        "seats": 25,
        "available_seats": 20,
        "is_active": True
    }

def valid_booking():
    return {
        "user_id": "507f1f77bcf86cd799439011",
        "schedule_id": "507f1f77bcf86cd799439022",
        "date": "2024-06-11",
        "time": "08:00",
        "status": "booked",
        "created_at": "2024-06-01T10:00:00"
    }

def valid_notification():
    return {
        "user_id": "507f1f77bcf86cd799439011",
        "message": "Your trip is due in 15 minutes!",
        "notif_type": "reminder",
        "sent": False,
        "created_at": "2024-06-01T09:45:00"
    }

def valid_payment():
    return {
        "user_id": "507f1f77bcf86cd799439011",
        "provider_id": "507f1f77bcf86cd799439012",
        "amount": 1200.0,
        "payment_time": "2024-06-01T10:01:00",
        "status": "completed"
    }

# Model schema unit tests
def test_user_schema_valid():
    data = valid_user()
    loaded = UserSchema().load(data)
    assert loaded["email"] == data["email"]
    assert loaded["user_type"] == "user"

def test_user_schema_invalid_phone():
    data = valid_user()
    data["phone"] = "123" # Too short!
    with pytest.raises(ValidationError):
        UserSchema().load(data)

def test_provider_schema_valid():
    data = valid_provider()
    loaded = ProviderSchema().load(data)
    assert loaded["provider_name"] == data["provider_name"]
    assert loaded["user_type"] == "provider"

def test_subscription_schema_valid():
    data = valid_subscription()
    loaded = SubscriptionSchema().load(data)
    assert loaded["plan_type"] == "monthly"

def test_schedule_schema_valid():
    data = valid_schedule()
    loaded = ScheduleSchema().load(data)
    assert "timings" in loaded
    assert "days" in loaded

def test_booking_schema_valid():
    data = valid_booking()
    loaded = BookingSchema().load(data)
    assert loaded["status"] == "booked"

def test_notification_schema_valid():
    data = valid_notification()
    loaded = NotificationSchema().load(data)
    assert loaded["notif_type"] == "reminder"

def test_payment_schema_valid():
    data = valid_payment()
    loaded = PaymentSchema().load(data)
    assert loaded["status"] == "completed"
