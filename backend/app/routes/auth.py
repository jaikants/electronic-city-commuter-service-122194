"""
Authentication routes for user and provider signup/login.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import get_db, UserSchema, ProviderSchema
from app.utils import hash_password, verify_password, create_token

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="User & Provider Authentication")

user_schema = UserSchema()
provider_schema = ProviderSchema()

# PUBLIC_INTERFACE
@blp.route("/signup/user")
class UserSignup(MethodView):
    """User registration endpoint."""
    def post(self):
        data = request.get_json()
        db = get_db()
        existing = db.users.find_one({"email": data.get("email")})
        if existing:
            return {"message": "User already exists"}, 409
        data["password"] = hash_password(data["password"])
        data["user_type"] = "user"
        db.users.insert_one(data)
        return {"message": "Signup successful."}, 201

# PUBLIC_INTERFACE
@blp.route("/signup/provider")
class ProviderSignup(MethodView):
    """Provider registration endpoint."""
    def post(self):
        data = request.get_json()
        db = get_db()
        existing = db.providers.find_one({"email": data.get("email")})
        if existing:
            return {"message": "Provider already exists"}, 409
        data["password"] = hash_password(data["password"])
        data["user_type"] = "provider"
        db.providers.insert_one(data)
        return {"message": "Provider signup successful"}, 201

# PUBLIC_INTERFACE
@blp.route("/login")
class Login(MethodView):
    """Login for users/providers."""
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        db = get_db()
        user = db.users.find_one({"email": email}) or db.providers.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            return {"message": "Invalid credentials"}, 401
        token = create_token(str(user["_id"]), user["user_type"])
        return {"access_token": token, "user_type": user['user_type']}, 200
