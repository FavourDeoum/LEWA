"""
LLM Service
Handles interactions with Groq API (replacing Gemini).
"""
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LLMService:
    def __init__(self):
        if not GROQ_API_KEY:
            print("WARNING: GROQ_API_KEY not found in environment variables.")
            self.client = None
        else:
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model = "llama-3.3-70b-versatile"  # High performance model

    async def generate_content(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates content using Groq (Llama 3.3).
        """
        if not self.client:
            return "Error: GROQ_API_KEY is missing. Please configure it in the .env file."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Singleton instance (keeping the name gemini_service to avoid refactoring all routers)
gemini_service = LLMService()
