from flask import Blueprint, render_template, request, jsonify, current_app
from bson import ObjectId
import json
from datetime import datetime
from app.models.database import Database

bp = Blueprint('history', __name__, url_prefix='/api')


@bp.route('/history')
def history():
    """Render the history panel page"""
    return render_template('history.html')


@bp.route('/history/conversations', methods=['GET'])
def get_conversations():
    """API endpoint to get all conversations for a user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        limit = int(request.args.get('limit', 50))
        
        db = Database()
        conversations = db.get_conversations(user_id, limit)
        
        # Convert ObjectId to string for JSON serialization
        for conv in conversations:
            conv['_id'] = str(conv['_id'])
            if isinstance(conv['created_at'], datetime):
                conv['created_at'] = conv['created_at'].isoformat()
            if isinstance(conv['updated_at'], datetime):
                conv['updated_at'] = conv['updated_at'].isoformat()
        
        # Close the database connection
        db.close()
        
        return jsonify({'conversations': conversations})
        
    except Exception as e:
        print(f"Error in get_conversations: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/history/conversation/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """API endpoint to delete a conversation"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        db = Database()
        
        # Verify the conversation belongs to the user
        conversation = db.get_conversation(ObjectId(conversation_id))
        if not conversation or conversation.get('user_id') != user_id:
            db.close()  # Close the connection before returning
            return jsonify({'error': 'Invalid conversation'}), 400
        
        # In a real app, you might want to delete associated messages too
        # For now, we'll just delete the conversation
        result = db.db.conversations.delete_one({'_id': ObjectId(conversation_id), 'user_id': user_id})
        
        if result.deleted_count == 0:
            db.close()  # Close the connection before returning
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Close the database connection
        db.close()
        
        return jsonify({'message': 'Conversation deleted successfully'})
        
    except Exception as e:
        print(f"Error in delete_conversation: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/history/conversations', methods=['DELETE'])
def delete_all_conversations():
    """API endpoint to delete all conversations for a user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        db = Database()
        
        # Delete all conversations for the user
        result = db.db.conversations.delete_many({'user_id': user_id})
        
        # In a real app, you might also want to delete associated messages
        
        # Close the database connection
        db.close()
        
        return jsonify({
            'message': f'{result.deleted_count} conversations deleted successfully'
        })
        
    except Exception as e:
        print(f"Error in delete_all_conversations: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500