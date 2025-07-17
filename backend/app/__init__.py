from flask import Flask
from flask_cors import CORS
from .routes.health import blp as health_blp
from flask_smorest import Api

# Import route blueprints
from .routes.auth import blp as auth_blp
from .routes.subscription import blp as subscription_blp
from .routes.schedule import blp as schedule_blp
from .routes.booking import blp as booking_blp
from .routes.notification import blp as notification_blp
from .routes.payment import blp as payment_blp
from .routes.profile import blp as profile_blp

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "Electronic City Commuter Service API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(auth_blp)
api.register_blueprint(subscription_blp)
api.register_blueprint(schedule_blp)
api.register_blueprint(booking_blp)
api.register_blueprint(notification_blp)
api.register_blueprint(payment_blp)
api.register_blueprint(profile_blp)
