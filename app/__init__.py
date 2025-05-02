from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # --- Session Config ---
    app.secret_key = 'supersecretkey123' 

    # --- MongoDB Config ---
    app.config["MONGO_URI"] = "mongodb://mongo:27017/UniQ"
    mongo.init_app(app)

    # --- Blueprints ---
    from app.routes.user_routes import user_bp
    from app.routes.student_routes import student_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
