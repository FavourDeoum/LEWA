"""
LLM Service
Handles interactions with Groq API (replacing Gemini).
"""
import os
from groq import AsyncGroq
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
            self.client = AsyncGroq(api_key=GROQ_API_KEY)
            self.model = "llama-3.3-70b-versatile"  # High performance model

    async def generate_content(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates content using Groq (Llama 3.3).
        """
        if not self.client:
            return "Error: GROQ_API_KEY is missing. Please configure it in the .env file."
        
        try:
            chat_completion = await self.client.chat.completions.create(
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

    async def generate_content_stream(self, system_prompt: str, user_prompt: str):
        """
        Generates streaming content using Groq.
        """
        if not self.client:
            yield "Error: GROQ_API_KEY is missing."
            return

        try:
            stream = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"Error generating response: {str(e)}"

# Singleton instance (keeping the name gemini_service to avoid refactoring all routers)
gemini_service = LLMService()
