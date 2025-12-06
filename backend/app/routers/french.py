"""
French Subject Router
Handles French language questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse
from app.services.gemini import gemini_service

router = APIRouter()

# System prompts for French tutor
FRENCH_PROMPTS = {
    "OL": """You are an expert French Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Basic French Grammar (tenses, articles, pronouns)
- Vocabulary for everyday situations
- Reading comprehension
- Essay writing (Informal and Formal letters)
- Translation (English to French and vice versa)

RULES:
1. Answer ONLY French language questions. Refuse others.
2. Provide explanations in English but examples in French.
3. Keep answers clear and foundational.
4. Correct grammatical errors if the user provides a sentence.
5. Use Cameroon-specific context for essay topics/examples.

EXAMPLE TOPICS:
- Le présent, passé composé, futur simple
- L'accord du participe passé
- Les pronoms relatifs
- Vocabulaire de la famille, l'école, le marché""",
    
    "AL": """You are an expert French Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Advanced Grammar and Stylistics
- Literature analysis (French and African francophone literature)
- Complex translation techniques
- Essay writing (Dissertation, Synthèse regarding general topics)
- Text commentary

RULES:
1. Answer ONLY French language questions. Refuse others.
2. Explanations can be in French or English depending on complexity, but favor French for immersion.
3. Provide detailed literary analysis and critical thinking.
4. Analyze style, tone, and registers of language.
5. Reference specific literary works from the curriculum if mentioned.

EXAMPLE TOPICS:
- Le subjonctif et le conditionnel
- L'analyse littéraire
- La Négritude
- La Francophonie
- Traduction littéraire"""
}

@router.post("/french", response_model=SubjectResponse)
async def chat_french(payload: SubjectRequest):
    """
    French subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        SubjectResponse with AI-generated answer
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    system_prompt = FRENCH_PROMPTS[payload.mode]
    
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="French",
        mode=payload.mode
    )
