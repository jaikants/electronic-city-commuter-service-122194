"""
Subscription management endpoints.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import get_db, SubscriptionSchema
from app.utils import login_required
from bson.objectid import ObjectId
import datetime

blp = Blueprint("Subscription", "subscription", url_prefix="/subscriptions", description="Subscription Management")

subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)

# PUBLIC_INTERFACE
@blp.route("/")
class SubscriptionList(MethodView):
    """Get all subscriptions for authenticated user. Or create a new one."""
    @login_required(user_type="user")
    def get(current_user):
        db = get_db()
        # Current user is user_id
        subs = list(db.subscriptions.find({"user_id": current_user}))
        for sub in subs:
            sub["id"] = str(sub["_id"])
        return subscriptions_schema.dump(subs), 200

    @login_required(user_type="user")
    def post(current_user):
        db = get_db()
        json_data = request.get_json()
        json_data["user_id"] = current_user
        json_data["start_date"] = datetime.date.today().isoformat()
        # Assume end_date provided, else calculate +1 month:
        if not json_data.get("end_date"):
            json_data["end_date"] = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
        db.subscriptions.insert_one(json_data)
        return {"message": "Subscription created"}, 201

# PUBLIC_INTERFACE
@blp.route("/<sub_id>/cancel")
class CancelSubscription(MethodView):
    """Cancel subscription."""
    @login_required(user_type="user")
    def post(current_user, sub_id):
        db = get_db()
        sub = db.subscriptions.find_one({"_id": ObjectId(sub_id), "user_id": current_user})
        if not sub:
            return {"message": "Not found"}, 404
        db.subscriptions.update_one({"_id": ObjectId(sub_id)}, {"$set": {"is_active": False}})
        return {"message": "Subscription cancelled"}, 200
