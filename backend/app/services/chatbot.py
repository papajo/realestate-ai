from typing import List, Dict
from app.core.config import settings
import os

# Optional ML imports
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    AutoTokenizer = None
    AutoModelForCausalLM = None
    torch = None


class ChatbotService:
    """NLP chatbot service using Hugging Face DialoGPT"""
    
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load DialoGPT model and tokenizer"""
        if not TRANSFORMERS_AVAILABLE:
            print("Warning: Transformers not available. Using fallback response system.")
            self.model = None
            self.tokenizer = None
            return
        
        try:
            # Use API if key is available, otherwise load locally
            if settings.HUGGINGFACE_API_KEY:
                from huggingface_hub import login
                login(token=settings.HUGGINGFACE_API_KEY)
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Set pad token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
        except Exception as e:
            print(f"Warning: Could not load DialoGPT model: {e}")
            print("Using fallback response system")
            self.model = None
            self.tokenizer = None
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None
    ) -> Dict:
        """Generate chatbot response"""
        if conversation_history is None:
            conversation_history = []
        
        # Qualification keywords
        qualification_keywords = {
            "positive": ["sell", "interested", "motivated", "need to sell", "quick sale", "as-is"],
            "negative": ["not interested", "not selling", "just looking", "not ready"]
        }
        
        # Check for qualification signals
        message_lower = user_message.lower()
        positive_signals = sum(1 for kw in qualification_keywords["positive"] if kw in message_lower)
        negative_signals = sum(1 for kw in qualification_keywords["negative"] if kw in message_lower)
        
        qualification_score = 0.5
        if positive_signals > negative_signals:
            qualification_score = min(1.0, 0.5 + (positive_signals * 0.15))
            qualification_status = "qualified"
        elif negative_signals > positive_signals:
            qualification_score = max(0.0, 0.5 - (negative_signals * 0.15))
            qualification_status = "not_qualified"
        else:
            qualification_status = "pending"
        
        # Generate response using model if available
        if TRANSFORMERS_AVAILABLE and self.model and self.tokenizer:
            response_text = self._generate_with_model(user_message, conversation_history)
        else:
            response_text = self._generate_fallback_response(user_message, qualification_score)
        
        return {
            "message": response_text,
            "qualification_detected": positive_signals > 0 or negative_signals > 0,
            "qualification_status": qualification_status,
            "qualification_score": qualification_score
        }
    
    def _generate_with_model(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Generate response using DialoGPT model"""
        if not TRANSFORMERS_AVAILABLE or not self.model or not self.tokenizer:
            return self._generate_fallback_response(user_message, 0.5)
        
        try:
            # Build conversation context
            context = ""
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context += f"{role}: {content}\n"
            
            context += f"user: {user_message}\nassistant:"
            
            # Tokenize
            inputs = self.tokenizer.encode(context, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
            return response.strip()
        except Exception as e:
            print(f"Error generating response with model: {e}")
            return self._generate_fallback_response(user_message, 0.5)
    
    def _generate_fallback_response(self, user_message: str, qualification_score: float) -> str:
        """Generate fallback response when model is not available"""
        message_lower = user_message.lower()
        
        if any(kw in message_lower for kw in ["sell", "selling", "interested"]):
            return "I understand you're interested in selling. Can you tell me more about your property and timeline?"
        elif any(kw in message_lower for kw in ["price", "value", "worth"]):
            return "I'd be happy to help you understand your property's value. What's the address of the property?"
        elif any(kw in message_lower for kw in ["when", "timeline", "how soon"]):
            return "Timing is important. Are you looking to sell quickly, or do you have flexibility?"
        else:
            return "Thank you for your interest. I'm here to help you with your real estate needs. What would you like to know?"

