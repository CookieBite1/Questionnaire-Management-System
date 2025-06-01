from flask import Flask
from flask_pymongo import PyMongo

import os 

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # --- Session Config ---
    app.secret_key = os.getenv("SECRET_KEY", "supersecretkey123")  # για Flask session

    # --- MongoDB Config ---
    mongo_host = os.getenv('MONGO_HOST', 'localhost')  # Default = localhost if not exists
    app.config["MONGO_URI"] = f"mongodb://{mongo_host}:27017/UniQ"
    mongo.init_app(app)

    # --- Blueprints ---
    from app.routes.user_routes import user_bp
    from app.routes.student_routes import student_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.main_routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
