"""
Gemini Service
Handles interactions with Google's Gemini Pro API.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiService:
    def __init__(self):
        if not GEMINI_API_KEY:
            # We allow initialization without key for CI/CD or build phases, 
            # but methods will fail if called.
            print("WARNING: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=GEMINI_API_KEY)
            # using gemini-2.0-flash as it is available in the user's account
            self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def generate_content(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates content using Gemini Pro.
        
        Args:
            system_prompt: The persona or rules for the AI.
            user_prompt: The user's input question or request.
            
        Returns:
            The generated text response.
        """
        if not GEMINI_API_KEY:
            return "Error: Gemini API key is missing. Please configure it in the .env file."
        
        try:
            # Gemini Pro doesn't have a distinct "system" role in the same way as ChatCompletions 
            # in some other APIs, but we can prepend the system instructions or use new system instruction features if available.
            # For standard gemini-pro, prepending context is reliable.
            
            full_prompt = f"{system_prompt}\n\nUser Question: {user_prompt}"
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                return "Error: Quota exceeded. Please try again in a moment. (Rate limit reached)"
            return f"Error generating response: {error_msg}"

# Singleton instance
gemini_service = GeminiService()
