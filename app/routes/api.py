from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
import json
from datetime import datetime
from app.models.database import Database

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and get responses from Gemini"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        conversation_id = data.get('conversation_id')  # Optional, for continuing a conversation
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Create a database instance for this request
        db = Database()
        
        # Create or get user
        user = db.get_user(user_id)
        if not user:
            db.create_user({
                'user_id': user_id,
                'created_at': datetime.utcnow()
            })
        
        # Determine conversation
        if conversation_id:
            # Use existing conversation
            conversation = db.get_conversation(ObjectId(conversation_id))
            if not conversation or conversation.get('user_id') != user_id:
                db.close()  # Close the connection before returning
                return jsonify({'error': 'Invalid conversation'}), 400
            
            # Get conversation history for context
            messages = db.get_messages(ObjectId(conversation_id))
            chat_service = current_app.config['GEMINI_SERVICE']  # Keeping config name for compatibility
            response_text = chat_service.chat_with_history(messages, user_message)
        else:
            # Create new conversation
            chat_service = current_app.config['GEMINI_SERVICE']  # Keeping config name for compatibility
            response_text = chat_service.get_chat_response(user_message)
            
            # Create a title for the conversation based on the first few words of user message
            title = user_message.strip()[:50] + "..." if len(user_message) > 50 else user_message.strip()
            if not title:
                title = "New Conversation"
                
            conversation_data = {
                'user_id': user_id,
                'title': title,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = db.create_conversation(conversation_data)
            conversation_id = result.inserted_id
        
        # Save user message
        user_message_data = {
            'conversation_id': ObjectId(conversation_id),
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.utcnow()
        }
        db.add_message(user_message_data)
        
        # Save assistant response
        assistant_message_data = {
            'conversation_id': ObjectId(conversation_id),
            'role': 'assistant',
            'content': response_text,
            'timestamp': datetime.utcnow()
        }
        db.add_message(assistant_message_data)
        
        # Update conversation's updated_at field
        db.update_conversation(ObjectId(conversation_id), {'updated_at': datetime.utcnow()})
        
        # Close the database connection
        db.close()
        
        return jsonify({
            'response': response_text,
            'conversation_id': str(conversation_id)
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations for a user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        db = Database()
        conversations = db.get_conversations(user_id)
        
        # Convert ObjectId to string for JSON serialization
        for conv in conversations:
            conv['_id'] = str(conv['_id'])
        
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


@bp.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get a specific conversation with its messages"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        db = Database()
        
        # Verify the conversation belongs to the user
        conversation = db.get_conversation(ObjectId(conversation_id))
        if not conversation or conversation.get('user_id') != user_id:
            db.close()  # Close the connection before returning
            return jsonify({'error': 'Invalid conversation'}), 400
        
        messages = db.get_messages(ObjectId(conversation_id))
        
        # Convert ObjectIds to strings for JSON serialization
        conversation['_id'] = str(conversation['_id'])
        for msg in messages:
            msg['_id'] = str(msg['_id'])
            msg['conversation_id'] = str(msg['conversation_id'])
        
        # Close the database connection
        db.close()
        
        return jsonify({
            'conversation': conversation,
            'messages': messages
        })
        
    except Exception as e:
        print(f"Error in get_conversation: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/new_conversation', methods=['POST'])
def new_conversation():
    """Start a new conversation"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        title = data.get('title', 'New Conversation')
        
        db = Database()
        
        conversation_data = {
            'user_id': user_id,
            'title': title,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db.create_conversation(conversation_data)
        
        # Close the database connection
        db.close()
        
        return jsonify({
            'conversation_id': str(result.inserted_id),
            'title': title
        })
        
    except Exception as e:
        print(f"Error in new_conversation: {str(e)}")
        # Make sure to close the database connection in case of exception
        try:
            db.close()
        except:
            pass  # Ignore error if db wasn't initialized
        return jsonify({'error': 'Internal server error'}), 500