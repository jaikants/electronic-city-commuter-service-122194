"""
Booking and cancellation endpoints.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import get_db, BookingSchema
from app.utils import login_required
from bson.objectid import ObjectId
import datetime

blp = Blueprint("Booking", "booking", url_prefix="/bookings", description="Booking & Cancellation")

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# PUBLIC_INTERFACE
@blp.route("/")
class BookingList(MethodView):
    """List your bookings or create a new one."""
    @login_required(user_type="user")
    def get(current_user):
        db = get_db()
        bookings = list(db.bookings.find({"user_id": current_user}))
        for b in bookings:
            b["id"] = str(b["_id"])
        return bookings_schema.dump(bookings), 200

    @login_required(user_type="user")
    def post(current_user):
        db = get_db()
        data = request.get_json()
        data["user_id"] = current_user
        # Check/adjust seat availability:
        schedule = db.schedules.find_one({"_id": ObjectId(data["schedule_id"])})
        if not schedule:
            return {"message": "Schedule not found"}, 404
        if schedule["available_seats"] <= 0:
            return {"message": "No seats available"}, 409
        db.schedules.update_one({"_id": ObjectId(data["schedule_id"])}, {"$inc": {"available_seats": -1}})
        data["status"] = "booked"
        data["created_at"] = datetime.datetime.utcnow().isoformat()
        db.bookings.insert_one(data)
        return {"message": "Booking successful"}, 201

# PUBLIC_INTERFACE
@blp.route("/<booking_id>/cancel")
class CancelBooking(MethodView):
    """Cancel a booking and release seat."""
    @login_required(user_type="user")
    def post(current_user, booking_id):
        db = get_db()
        booking = db.bookings.find_one({"_id": ObjectId(booking_id), "user_id": current_user})
        if not booking or booking["status"] == "cancelled":
            return {"message": "Booking not found or already cancelled"}, 404
        db.bookings.update_one({"_id": ObjectId(booking_id)}, {"$set": {"status": "cancelled"}})
        # Release seat if booking was for a future date
        db.schedules.update_one({"_id": ObjectId(booking["schedule_id"])}, {"$inc": {"available_seats": 1}})
        return {"message": "Booking cancelled"}, 200
