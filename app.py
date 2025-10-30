import os
from flask import Flask
from app.models.database import Database
from app.utils.gemini_service import ChatService
from app.utils.data_analysis_service import DataAnalysisService


def create_app():
    # Use the templates and static folders from the app subdirectory
    app = Flask(__name__,
                template_folder='app/templates',
                static_folder='app/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/chatbot_db')
    
    # Initialize services
    try:
        chat_service = ChatService()  # Ollama Qwen2.5 as primary with Gemini as fallback
    except Exception as e:
        print(f"Error initializing Ollama/Gemini service: {e}")
        raise
    
    data_analysis_service = DataAnalysisService()
    
    # Store services in app config for access in routes
    app.config['GEMINI_SERVICE'] = chat_service  # Keep the config name for compatibility
    app.config['DATA_ANALYSIS_SERVICE'] = data_analysis_service
    
    # Import and register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.history import bp as history_bp
    app.register_blueprint(history_bp)
    
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    from app.routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp)
    
    return app


# For running the application directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)