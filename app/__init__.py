import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/chatbot_db')
    app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', '')
    
    # Import and register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.history import bp as history_bp
    app.register_blueprint(history_bp)
    
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    return app