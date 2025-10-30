import google.generativeai as genai
import os
from dotenv import load_dotenv
from .ollama_service import OllamaService
from .format_utils import clean_response_format

load_dotenv()

class ChatService:
    def __init__(self):
        # Initialize Ollama as primary service
        self.ollama_service = OllamaService()
        
        # Check if Gemini API key is available for fallback
        api_key = os.getenv('GEMINI_API_KEY')
        self.use_gemini = False
        self.model = None
        
        if api_key and api_key.strip() != '':
            try:
                genai.configure(api_key=api_key)
                # Try common gemini models for fallback
                available_models = ['gemini-2.5-flash', 'gemini-pro', 'gemini-1.0-pro',]
                
                for model_name in available_models:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"Gemini API available as fallback with model: {model_name}")
                        self.use_gemini = True
                        break
                    except:
                        continue
                
                if not self.use_gemini:
                    print("No available Gemini model found for fallback")
                    
            except Exception as e:
                print(f"Error initializing Gemini as fallback: {str(e)}")
        else:
            print("GEMINI_API_KEY not provided, Ollama Qwen2.5 will be used as primary (no fallback)")
    
    def get_chat_response(self, user_input: str) -> str:
        """
        Get a response from the Ollama Qwen2.5 model for DSA algorithm explanations,
        with fallback to Gemini if Ollama is not available
        """
        # Try Ollama first (as primary)
        try:
            response = self.ollama_service.get_chat_response(user_input)
            # Check if Ollama failed to provide a valid response
            if not response or "Error" in response or "error" in response or "connecting to Ollama" in response.lower():
                print("Ollama failed, falling back to Gemini")
                # Fallback to Gemini if available
                if self.use_gemini and self.model:
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
                        
                        gemini_response = self.model.generate_content(prompt)
                        cleaned_response = clean_response_format(gemini_response.text)
                        return cleaned_response
                    except Exception as e:
                        print(f"Error getting response from Gemini: {str(e)}")
                        cleaned_response = clean_response_format(response)  # Return Ollama error if Gemini also fails
                        return cleaned_response
            cleaned_response = clean_response_format(response)
            return cleaned_response
        except Exception as e:
            print(f"Error getting response from Ollama: {str(e)}")
            print("Falling back to Gemini service")
            # Fallback to Gemini if available
            if self.use_gemini and self.model:
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
                    
                    gemini_response = self.model.generate_content(prompt)
                    cleaned_response = clean_response_format(gemini_response.text)
                    return cleaned_response
                except Exception as gemini_e:
                    print(f"Error getting response from Gemini: {str(gemini_e)}")
                    cleaned_response = clean_response_format(f"Error: Could not get response from either Ollama or Gemini services.")
                    return cleaned_response
            else:
                cleaned_response = clean_response_format(f"Error: Ollama service failed and no Gemini fallback available: {str(e)}")
                return cleaned_response
    
    def chat_with_history(self, conversation_history: list, user_input: str) -> str:
        """
        Get a response considering the conversation history,
        with Ollama as primary and fallback to Gemini if needed
        """
        # Try Ollama first (as primary)
        try:
            response = self.ollama_service.chat_with_history(conversation_history, user_input)
            # Check if Ollama failed to provide a valid response
            if not response or "Error" in response or "error" in response or "connecting to Ollama" in response.lower():
                print("Ollama failed, falling back to Gemini")
                # Fallback to Gemini if available
                if self.use_gemini and self.model:
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
                        
                        gemini_response = self.model.generate_content(prompt)
                        cleaned_response = clean_response_format(gemini_response.text)
                        return cleaned_response
                    except Exception as e:
                        print(f"Error getting response from Gemini: {str(e)}")
                        cleaned_response = clean_response_format(response)  # Return Ollama error if Gemini also fails
                        return cleaned_response
            cleaned_response = clean_response_format(response)
            return cleaned_response
        except Exception as e:
            print(f"Error getting response from Ollama: {str(e)}")
            print("Falling back to Gemini service")
            # Fallback to Gemini if available
            if self.use_gemini and self.model:
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
                    
                    gemini_response = self.model.generate_content(prompt)
                    cleaned_response = clean_response_format(gemini_response.text)
                    return cleaned_response
                except Exception as gemini_e:
                    print(f"Error getting response from Gemini: {str(gemini_e)}")
                    cleaned_response = clean_response_format(f"Error: Could not get response from either Ollama or Gemini services.")
                    return cleaned_response
            else:
                cleaned_response = clean_response_format(f"Error: Ollama service failed and no Gemini fallback available: {str(e)}")
                return cleaned_response