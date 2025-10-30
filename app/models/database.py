from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, mongo_uri=None):
        # Connect to MongoDB
        self.client = MongoClient(mongo_uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
        self.db = self.client['chatbot_db']
        
        # Collections
        self.users = self.db['users']
        self.conversations = self.db['conversations']
        self.messages = self.db['messages']
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for better query performance"""
        # Index for user_id in conversations
        self.conversations.create_index([('user_id', 1)])
        
        # Index for conversation_id in messages
        self.messages.create_index([('conversation_id', 1)])
        
        # Index for timestamp in messages for sorting
        self.messages.create_index([('timestamp', -1)])
        
        # Index for conversation title for search
        self.conversations.create_index([('title', 'text')])
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.find_one({'user_id': user_id})
    
    def create_user(self, user_data):
        """Create a new user"""
        return self.users.insert_one(user_data)
    
    def get_conversations(self, user_id, limit=50):
        """Get conversations for a user"""
        return list(self.conversations.find({'user_id': user_id}).sort('_id', -1).limit(limit))
    
    def get_conversation(self, conversation_id):
        """Get a specific conversation by ID"""
        return self.conversations.find_one({'_id': conversation_id})
    
    def create_conversation(self, conversation_data):
        """Create a new conversation"""
        return self.conversations.insert_one(conversation_data)
    
    def update_conversation(self, conversation_id, update_data):
        """Update a conversation"""
        return self.conversations.update_one({'_id': conversation_id}, {'$set': update_data})
    
    def get_messages(self, conversation_id):
        """Get messages for a conversation"""
        return list(self.messages.find({'conversation_id': conversation_id}).sort('timestamp', 1))
    
    def add_message(self, message_data):
        """Add a message to a conversation"""
        return self.messages.insert_one(message_data)
    
    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()