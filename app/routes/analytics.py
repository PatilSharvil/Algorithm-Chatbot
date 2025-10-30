from flask import Blueprint, jsonify, current_app
from bson import ObjectId
from app.models.database import Database

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api')


@analytics_bp.route('/usage', methods=['GET'])
def get_usage_analytics():
    """Get usage analytics for the application"""
    try:
        user_id = 'default_user'  # In a real app, this would come from auth
        
        db = Database()
        data_analysis_service = current_app.config['DATA_ANALYSIS_SERVICE']
        
        # Get all conversations for the user
        conversations = db.get_conversations(user_id, limit=1000)  # Get more conversations for analytics
        
        # Get all messages for the user (this might need to be optimized for large datasets)
        all_messages = []
        for conv in conversations:
            messages = db.get_messages(conv['_id'])
            for msg in messages:
                msg['conversation_title'] = conv.get('title', 'Untitled')
            all_messages.extend(messages)
        
        # Perform analytics using our data analysis service
        engagement_data = data_analysis_service.analyze_user_engagement(conversations, all_messages)
        time_series_data = data_analysis_service.generate_time_series_analysis(conversations)
        
        # Close the database connection
        db.close()
        
        return jsonify({
            'engagement': engagement_data,
            'time_series': time_series_data,
            'total_conversations': len(conversations),
            'total_messages': len(all_messages)
        })
        
    except Exception as e:
        print(f"Error in analytics endpoint: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500


# Register this blueprint in the create_app function
def register_analytics(app):
    app.register_blueprint(analytics_bp, url_prefix='/api')