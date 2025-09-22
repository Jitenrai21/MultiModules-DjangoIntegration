"""
LLM Service Layer for handling different AI model providers
Supports Ollama (local) and Gemini (cloud) with automatic fallback
"""
import requests
import json
import logging
from typing import Optional, Dict, Any
from django.conf import settings
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

class LLMServiceError(Exception):
    """Custom exception for LLM service errors"""
    pass

class BaseLLMProvider:
    """Base class for LLM providers"""
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError
    
    def is_available(self) -> bool:
        raise NotImplementedError

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3:latest"):
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using Ollama API"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "top_p": kwargs.get("top_p", 0.9),
                    "max_tokens": kwargs.get("max_tokens", 2000)
                }
            }
            
            logger.info(f"Sending request to Ollama: {self.api_url}")
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120  # 2 minutes timeout for local generation
            )
            response.raise_for_status()
            
            data = response.json()
            if "response" in data:
                logger.info("Successfully received response from Ollama")
                return data["response"].strip()
            else:
                raise LLMServiceError(f"Invalid response format from Ollama: {data}")
                
        except requests.exceptions.ConnectionError:
            raise LLMServiceError("Cannot connect to Ollama server. Make sure 'ollama serve' is running.")
        except requests.exceptions.Timeout:
            raise LLMServiceError("Ollama request timed out. The model might be processing a complex request.")
        except requests.exceptions.RequestException as e:
            raise LLMServiceError(f"Ollama API error: {str(e)}")
        except Exception as e:
            raise LLMServiceError(f"Unexpected error with Ollama: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Ollama server is available"""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except:
            return False

class GeminiProvider(BaseLLMProvider):
    """Google Gemini API provider (fallback)"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model_name = model
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.chat_session = self.model.start_chat(history=[])
        else:
            self.model = None
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using Gemini API"""
        if not self.model:
            raise LLMServiceError("Gemini API key not configured")
        
        try:
            response = self.chat_session.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            raise LLMServiceError(f"Gemini API error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return self.api_key is not None and self.model is not None

class LLMService:
    """
    Main LLM service that handles provider selection and fallback
    """
    
    def __init__(self, primary_provider: str = "ollama"):
        self.primary_provider = primary_provider
        self.providers = {
            "ollama": OllamaProvider(
                base_url=getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434'),
                model=getattr(settings, 'OLLAMA_MODEL', 'llama3:latest')
            ),
            "gemini": GeminiProvider()
        }
        
        # Chat session management for maintaining context
        self.chat_sessions = {}
    
    def get_available_provider(self) -> BaseLLMProvider:
        """Get the first available provider, starting with primary"""
        # Try primary provider first
        if self.primary_provider in self.providers:
            provider = self.providers[self.primary_provider]
            if provider.is_available():
                logger.info(f"Using primary provider: {self.primary_provider}")
                return provider
        
        # Try fallback providers
        for name, provider in self.providers.items():
            if name != self.primary_provider and provider.is_available():
                logger.warning(f"Primary provider unavailable, using fallback: {name}")
                return provider
        
        raise LLMServiceError("No LLM providers are available")
    
    def generate_response(self, prompt: str, session_id: Optional[str] = None, **kwargs) -> str:
        """
        Generate response using the best available provider
        
        Args:
            prompt: The input prompt
            session_id: Optional session ID for context management
            **kwargs: Additional generation parameters
        
        Returns:
            Generated response text
        """
        provider = self.get_available_provider()
        
        try:
            # For session-based conversations, you might want to add context
            if session_id and session_id in self.chat_sessions:
                # Add previous context if needed
                full_prompt = self._build_contextual_prompt(prompt, session_id)
            else:
                full_prompt = prompt
            
            response = provider.generate_response(full_prompt, **kwargs)
            
            # Store response in session if session_id provided
            if session_id:
                if session_id not in self.chat_sessions:
                    self.chat_sessions[session_id] = []
                self.chat_sessions[session_id].append({
                    "prompt": prompt,
                    "response": response,
                    "provider": provider.__class__.__name__
                })
            
            return response
            
        except LLMServiceError:
            raise
        except Exception as e:
            raise LLMServiceError(f"Unexpected error generating response: {str(e)}")
    
    def _build_contextual_prompt(self, prompt: str, session_id: str) -> str:
        """Build prompt with conversation context"""
        # This is a simple implementation - you can enhance it based on your needs
        session_history = self.chat_sessions.get(session_id, [])
        
        # Only include last few exchanges to avoid token limits
        recent_history = session_history[-3:] if len(session_history) > 3 else session_history
        
        context_parts = []
        for exchange in recent_history:
            context_parts.append(f"User: {exchange['prompt']}")
            context_parts.append(f"Assistant: {exchange['response']}")
        
        if context_parts:
            context = "\n".join(context_parts)
            return f"Previous conversation:\n{context}\n\nCurrent user message: {prompt}"
        else:
            return prompt
    
    def clear_session(self, session_id: str):
        """Clear chat session history"""
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers"""
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                "available": provider.is_available(),
                "type": provider.__class__.__name__
            }
        return status

# Global instance
llm_service = LLMService()