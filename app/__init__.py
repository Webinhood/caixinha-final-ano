from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///raffle.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
