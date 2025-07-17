"""
Models and helper classes for Electronic City commuter service backend.

Implements schema validation using marshmallow for:
- Users
- Providers
- Subscriptions
- Trips/Schedules
- Bookings
- Notifications
- Payments
- Profile management

MongoDB collections are accessed via PyMongo, with marshmallow used for input/output validation.
"""
from pymongo import MongoClient
from marshmallow import Schema, fields, validate
import os

def get_db():
    """MongoDB client/utility - gets the current database."""
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
    mongo_db = os.environ.get('MONGO_DB', 'commuter_service')
    client = MongoClient(mongo_uri)
    return client[mongo_db]

# PUBLIC_INTERFACE
class UserSchema(Schema):
    """Schema for Users (commuters)."""
    id = fields.Str(dump_only=True, description="MongoDB user ID")
    email = fields.Email(required=True, description="User email")
    password = fields.Str(load_only=True, required=True, description="Password (hashed in db)")
    name = fields.Str(required=True, description="Full name")
    phone = fields.Str(required=True, validate=validate.Length(equal=10), description="Phone number")
    user_type = fields.Str(required=True, validate=validate.OneOf(["user"]), missing="user", description="User type: 'user'")
    profile_picture = fields.Str(description="Profile picture URL")
    subscriptions = fields.List(fields.Str(), description="List of subscription IDs")
    is_active = fields.Bool(missing=True, description="Account is active")

# PUBLIC_INTERFACE
class ProviderSchema(Schema):
    """Schema for Transport Providers."""
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    provider_name = fields.Str(required=True)
    phone = fields.Str(required=True, validate=validate.Length(equal=10))
    user_type = fields.Str(required=True, validate=validate.OneOf(["provider"]), missing="provider")
    service_routes = fields.List(fields.Str(), description="Service routes operated")
    schedules = fields.List(fields.Str(), description="List of schedule IDs")
    is_active = fields.Bool(missing=True)

# PUBLIC_INTERFACE
class SubscriptionSchema(Schema):
    """Schema for Subscription objects."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    provider_id = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    is_active = fields.Bool()
    plan_type = fields.Str(required=True, description="Plan type (e.g., monthly, quarterly)")
    amount = fields.Float(required=True)
    payment_id = fields.Str(required=True)

# PUBLIC_INTERFACE
class ScheduleSchema(Schema):
    """Schema for Trip Schedules."""
    id = fields.Str(dump_only=True)
    provider_id = fields.Str(required=True)
    route = fields.Str(required=True)
    timings = fields.List(fields.Time(), description="Timings (HH:MM format)")
    days = fields.List(fields.Str(), description="Days e.g. ['Mon', 'Tue', ...]")
    seats = fields.Int(required=True)
    available_seats = fields.Int(required=True)
    is_active = fields.Bool()

# PUBLIC_INTERFACE
class BookingSchema(Schema):
    """Schema for a Booking."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    schedule_id = fields.Str(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    status = fields.Str(validate=validate.OneOf(["booked", "cancelled"]), default="booked")
    created_at = fields.DateTime()

# PUBLIC_INTERFACE
class NotificationSchema(Schema):
    """Notifications/reminders."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    message = fields.Str(required=True)
    notif_type = fields.Str(validate=validate.OneOf(["reminder", "info", "alert"]))
    sent = fields.Bool(default=False)
    created_at = fields.DateTime()

# PUBLIC_INTERFACE
class PaymentSchema(Schema):
    """Payment data."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    provider_id = fields.Str(required=True)
    booking_id = fields.Str()
    subscription_id = fields.Str()
    amount = fields.Float(required=True)
    payment_time = fields.DateTime()
    transaction_id = fields.Str()
    status = fields.Str(validate=validate.OneOf(["pending", "completed", "failed"]), default="pending")

