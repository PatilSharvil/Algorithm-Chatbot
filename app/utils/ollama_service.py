import requests
import os
from typing import Optional
from .format_utils import clean_response_format


class OllamaService:
    def __init__(self):
        # Use Ollama URL from environment variable or default to localhost
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        # Default to Qwen2.5 model - can be overridden via environment variable
        self.model_name = os.getenv('OLLAMA_MODEL', 'qwen2.5:latest')  # Default to qwen2.5:latest
    
    def get_chat_response(self, user_input: str) -> str:
        """
        Get a response from the local Ollama model for DSA algorithm explanations
        """
        try:
            # Create a prompt that focuses on algorithmic explanations without code
            prompt = f"""
            As a DSA expert, please explain the algorithmic approach to solve this problem:
            {user_input}
            
            Focus on:
            1. Algorithmic approach
            2. Time and space complexity
            3. Data structures to use
            4. Step-by-step thought process
            5. Do NOT provide actual code implementation
            6. Only provide the approach and explanation
            7. Format the response in a clean, readable way with proper markdown-style formatting (use * or - for lists, ** for bold text, and avoid HTML tags like <strong>)
            """
            
            # Prepare the request to Ollama API
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60  # 60 second timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                raw_response = result.get('response', 'No response generated.')
                # Clean up the response format
                cleaned_response = clean_response_format(raw_response)
                return cleaned_response
            else:
                return f"Error from Ollama: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Error getting response from Ollama: {str(e)}"
    
    def chat_with_history(self, conversation_history: list, user_input: str) -> str:
        """
        Get a response considering the conversation history
        """
        try:
            # Format the conversation history for context
            history_context = ""
            for msg in conversation_history[-5:]:  # Use last 5 exchanges for context
                role = "User" if msg.get('role') == 'user' else "Assistant"
                history_context += f"{role}: {msg.get('content')}\n\n"
            
            prompt = f"""
            Previous conversation context:
            {history_context}
            
            Current question: {user_input}
            
            As a DSA expert, please explain the algorithmic approach to solve this problem, considering the context if relevant:
            
            Focus on:
            1. Algorithmic approach
            2. Time and space complexity
            3. Data structures to use
            4. Step-by-step thought process
            5. Do NOT provide actual code implementation
            6. Only provide the approach and explanation
            7. Format the response in a clean, readable way with proper markdown-style formatting (use * or - for lists, ** for bold text, and avoid HTML tags like <strong>)
            """
            
            # Prepare the request to Ollama API
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60  # 60 second timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                raw_response = result.get('response', 'No response generated.')
                # Clean up the response format
                cleaned_response = clean_response_format(raw_response)
                return cleaned_response
            else:
                return f"Error from Ollama: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Error getting response from Ollama: {str(e)}"