import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import json


class DataAnalysisService:
    def __init__(self):
        pass
    
    def analyze_conversation_metrics(self, conversations: List[Dict]) -> Dict[str, Any]:
        """
        Analyze conversation metrics using Pandas
        """
        if not conversations:
            return {
                'total_conversations': 0,
                'avg_conversations_per_day': 0,
                'peak_activity_day': None
            }
        
        # Convert conversations to DataFrame for analysis
        df = pd.DataFrame(conversations)
        
        # Convert created_at to datetime if it's not already
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Calculate metrics
        total_conversations = len(df)
        
        # Group by date to get daily activity
        df['date'] = df['created_at'].dt.date
        daily_activity = df.groupby('date').size()
        
        if len(daily_activity) > 0:
            avg_conversations_per_day = daily_activity.mean()
            peak_activity_day = daily_activity.idxmax().isoformat() if len(daily_activity) > 0 else None
        else:
            avg_conversations_per_day = 0
            peak_activity_day = None
        
        return {
            'total_conversations': total_conversations,
            'avg_conversations_per_day': round(avg_conversations_per_day, 2),
            'peak_activity_day': peak_activity_day
        }
    
    def analyze_message_patterns(self, messages: List[Dict]) -> Dict[str, Any]:
        """
        Analyze message patterns using NumPy and Pandas
        """
        if not messages:
            return {
                'total_messages': 0,
                'avg_message_length': 0,
                'user_vs_assistant_ratio': 0
            }
        
        df = pd.DataFrame(messages)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate message lengths
        df['message_length'] = df['content'].apply(lambda x: len(x) if x else 0)
        
        total_messages = len(df)
        avg_message_length = df['message_length'].mean()
        
        # Calculate user vs assistant ratio
        user_msg_count = len(df[df['role'] == 'user'])
        assistant_msg_count = len(df[df['role'] == 'assistant'])
        
        user_vs_assistant_ratio = user_msg_count / assistant_msg_count if assistant_msg_count > 0 else float('inf')
        
        return {
            'total_messages': total_messages,
            'avg_message_length': round(avg_message_length, 2),
            'user_vs_assistant_ratio': round(user_vs_assistant_ratio, 2)
        }
    
    def generate_time_series_analysis(self, conversations: List[Dict]) -> Dict[str, Any]:
        """
        Generate time series analysis of user activity
        """
        if not conversations:
            return {'activity_trend': [], 'busy_hours': []}
        
        df = pd.DataFrame(conversations)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Group by hour to find busiest hours
        df['hour'] = df['created_at'].dt.hour
        hourly_activity = df.groupby('hour').size().sort_values(ascending=False)
        
        # Group by date for trend analysis
        df['date'] = df['created_at'].dt.date
        daily_trend = df.groupby('date').size()
        
        return {
            'activity_trend': daily_trend.to_dict(),
            'busy_hours': hourly_activity.to_dict()
        }
    
    def analyze_user_engagement(self, conversations: List[Dict], messages: List[Dict]) -> Dict[str, Any]:
        """
        Analyze user engagement patterns
        """
        conv_metrics = self.analyze_conversation_metrics(conversations)
        msg_metrics = self.analyze_message_patterns(messages)
        
        return {
            'conversations': conv_metrics,
            'messages': msg_metrics
        }