from flask import Flask, Blueprint
from flask_cors import CORS
from .routes import userRoutes, adminRoutes, applicationRoutes
app = Flask(__name__)
cors = CORS(app)
app.config["SECRET_KEY"] = "dAmNSimPLeSecREtKeY"
app.config["CORS_ORIGIN_WHITELIST"] = ["*"]

origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
cors.init_app(userRoutes.bp, origins=origins)
cors.init_app(adminRoutes.admin, origins=origins)
cors.init_app(applicationRoutes.bp, origins=origins)
app.register_blueprint(userRoutes.bp)
app.register_blueprint(adminRoutes.admin)
app.register_blueprint(applicationRoutes.bp)