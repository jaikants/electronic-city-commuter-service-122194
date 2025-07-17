"""
Profile management for users and providers.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import get_db, UserSchema, ProviderSchema
from app.utils import login_required
from bson.objectid import ObjectId

blp = Blueprint("Profile", "profile", url_prefix="/profile", description="Profile Management")

user_schema = UserSchema()
provider_schema = ProviderSchema()

# PUBLIC_INTERFACE
@blp.route("/")
class MyProfile(MethodView):
    """Get and update the current profile."""
    @login_required()
    def get(current_user):
        db = get_db()
        user = db.users.find_one({"_id": ObjectId(current_user)})
        if not user:
            user = db.providers.find_one({"_id": ObjectId(current_user)})
            if not user:
                return {"message": "Not found"}, 404
            data = provider_schema.dump(user)
            data["id"] = str(user["_id"])
            return data, 200
        data = user_schema.dump(user)
        data["id"] = str(user["_id"])
        return data, 200

    @login_required()
    def put(current_user):
        db = get_db()
        json_data = request.get_json()
        user = db.users.find_one({"_id": ObjectId(current_user)})
        if user:
            db.users.update_one({"_id": ObjectId(current_user)}, {"$set": json_data})
            return {"message": "Profile updated"}, 200
        provider = db.providers.find_one({"_id": ObjectId(current_user)})
        if provider:
            db.providers.update_one({"_id": ObjectId(current_user)}, {"$set": json_data})
            return {"message": "Profile updated"}, 200
        return {"message": "Not found"}, 404
