from datetime import datetime
from bson import ObjectId
from typing import List, Optional


class User:
    def __init__(self, user_id: str, username: str = None, email: str = None, created_at: datetime = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            email=data.get('email'),
            created_at=data.get('created_at')
        )


class Message:
    def __init__(self, conversation_id: ObjectId, role: str, content: str, timestamp: datetime = None):
        self.conversation_id = conversation_id
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self):
        return {
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            conversation_id=data.get('conversation_id'),
            role=data.get('role'),
            content=data.get('content'),
            timestamp=data.get('timestamp')
        )


class Conversation:
    def __init__(self, user_id: str, title: str, created_at: datetime = None, updated_at: datetime = None):
        self.id = None
        self.user_id = user_id
        self.title = title
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        result = {
            'user_id': self.user_id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self.id:
            result['_id'] = self.id
        return result
    
    @classmethod
    def from_dict(cls, data):
        conv = cls(
            user_id=data.get('user_id'),
            title=data.get('title'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
        conv.id = data.get('_id')
        return conv