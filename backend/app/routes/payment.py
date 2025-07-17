"""
Payment integration endpoints.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import get_db, PaymentSchema
from app.utils import login_required
import datetime

blp = Blueprint("Payment", "payment", url_prefix="/payments", description="Payment Integration")

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

# PUBLIC_INTERFACE
@blp.route("/")
class PaymentList(MethodView):
    """List user or provider payments."""
    @login_required()
    def get(current_user):
        db = get_db()
        # Check if user or provider
        payments = list(db.payments.find({"$or": [{"user_id": current_user}, {"provider_id": current_user}]}))
        for p in payments:
            p["id"] = str(p["_id"])
        return payments_schema.dump(payments), 200

    @login_required(user_type="user")
    def post(current_user):
        """Make a payment (simulation)."""
        db = get_db()
        data = request.get_json()
        data["user_id"] = current_user
        data["payment_time"] = datetime.datetime.utcnow().isoformat()
        data["status"] = "completed" # Assume always success (for demo/proto)
        data["transaction_id"] = f"TXN{datetime.datetime.utcnow().timestamp()}"
        db.payments.insert_one(data)
        return {"message": "Payment successful"}, 201
