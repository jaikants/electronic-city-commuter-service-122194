"""
Notifications and reminders endpoints.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from app.models import get_db, NotificationSchema
from app.utils import login_required
from bson.objectid import ObjectId
import datetime

blp = Blueprint("Notification", "notification", url_prefix="/notifications", description="Trip Reminders & Notifications")

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)

# PUBLIC_INTERFACE
@blp.route("/")
class NotificationList(MethodView):
    """List notifications for current user."""
    @login_required()
    def get(current_user):
        db = get_db()
        notifs = list(db.notifications.find({"user_id": current_user}))
        for n in notifs:
            n["id"] = str(n["_id"])
        return notifications_schema.dump(notifs), 200

    @login_required()
    def post(current_user):
        """User or admin can post/send a notification to user (internal use)."""
        db = get_db()
        from flask import request
        data = request.get_json()
        data["user_id"] = current_user
        data["created_at"] = datetime.datetime.utcnow().isoformat()
        db.notifications.insert_one(data)
        return {"message": "Notification sent"}, 201

# PUBLIC_INTERFACE
@blp.route("/<notif_id>/mark_read")
class MarkNotificationRead(MethodView):
    """Mark as sent/read (internal for real-time/reminder features)."""
    @login_required()
    def post(current_user, notif_id):
        db = get_db()
        notif = db.notifications.find_one({"_id": ObjectId(notif_id), "user_id": current_user})
        if not notif:
            return {"message": "Not found"}, 404
        db.notifications.update_one({"_id": ObjectId(notif_id)}, {"$set": {"sent": True}})
        return {"message": "Marked as read"}, 200
