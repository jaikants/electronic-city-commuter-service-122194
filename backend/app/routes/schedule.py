"""
Schedule browsing and management endpoints.
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import get_db, ScheduleSchema
from app.utils import login_required
from bson.objectid import ObjectId

blp = Blueprint("Schedule", "schedule", url_prefix="/schedules", description="Trip Schedule Browsing")

schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)

# PUBLIC_INTERFACE
@blp.route("/")
class ScheduleList(MethodView):
    """Browse schedules (user) or view all owned (provider)."""
    @login_required()
    def get(current_user):
        db = get_db()
        provider = db.providers.find_one({"_id": ObjectId(current_user)})
        query = {}
        if provider:
            query = {"provider_id": current_user}
        schedules = list(db.schedules.find(query))
        for sched in schedules:
            sched["id"] = str(sched["_id"])
        return schedules_schema.dump(schedules), 200

    @login_required(user_type="provider")
    def post(current_provider):
        """Provider adds a schedule."""
        db = get_db()
        data = request.get_json()
        data["provider_id"] = current_provider
        db.schedules.insert_one(data)
        return {"message": "Schedule created"}, 201

# PUBLIC_INTERFACE
@blp.route("/<schedule_id>")
class ScheduleDetail(MethodView):
    """Get a single schedule detail."""
    @login_required()
    def get(current_user, schedule_id):
        db = get_db()
        sched = db.schedules.find_one({"_id": ObjectId(schedule_id)})
        if not sched:
            return {"message": "Not found"}, 404
        sched["id"] = str(sched["_id"])
        return schedule_schema.dump(sched), 200
