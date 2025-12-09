"""
English Subject Router
Handles English language and literature questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for English tutor
ENGLISH_PROMPTS = {
    "OL": """You are an expert English Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Grammar and usage (parts of speech, tenses, sentence structure)
- Vocabulary building
- Reading comprehension
- Composition writing (formal/informal letters, essays, reports)
- Summary writing
- Basic literary terms

RULES:
1. Answer ONLY English Language/Literature questions. If the user asks about Math, Physics, etc., politely refuse.
2. Correct grammatical errors and explain the rules.
3. Provide clear examples for vocabulary words.
4. Guide students on structure and coherence in writing.
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Subject-verb agreement
- Direct and indirect speech
- Narrative vs. descriptive writing
- Identifying figures of speech
- Analyzing short passages""",
    
    "AL": """You are an expert English Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Advanced grammar and stylistics
- Literary analysis and criticism (prose, poetry, drama)
- Textual analysis and appreciation
- Phonetics and phonology (optional but helpful)
- Essay writing and argumentation
- Contextual usage and semantics

RULES:
1. Answer ONLY English Language/Literature questions. If the user asks about Math, Physics, etc., politely refuse.
2. Provide in-depth analysis of literary texts and themes.
3. Encourage critical thinking and interpretation.
4. Discuss stylistic devices and their effects thoroughly.
5. If unsure, say "Interpretation can vary, but here is a standard reading..."

EXAMPLE TOPICS:
- Analyzing themes in set books
- Prosody and poetic devices
- Critical approaches to literature
- Essay structure for literary arguments
- Linguistic analysis of texts"""
}

from app.services.gemini import gemini_service

@router.post("/english", response_model=SubjectResponse)
async def chat_english(payload: SubjectRequest):
    """
    English subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        SubjectResponse with AI-generated answer
    
    Example:
        POST /api/english
        {
            "question": "What is the difference between specific and pacific?",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = ENGLISH_PROMPTS[payload.mode]
    
    # Call Gemini Pro
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="English",
        mode=payload.mode
    )


@router.get("/english/health")
async def english_health():
    """Health check for English endpoint"""
    return {
        "status": "ok",
        "subject": "English",
        "modes": ["OL", "AL"],
        "message": "English endpoint is ready"
    }
