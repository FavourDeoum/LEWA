"""
History Subject Router
Handles history questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for History tutor
HISTORY_PROMPTS = {
    "OL": """You are an expert History Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- History of Cameroon (Pre-colonial, Colonial, Post-colonial)
- African History (Slave trade, Scramble for Africa, Independence movements)
- World History (World Wars, Cold War, International Organizations)
- Social and Economic History

RULES:
1. Answer ONLY History questions. If the user asks about Math, Geography, Biology, etc., politely refuse and tell them to switch subjects.
2. Use specific dates, names, and events where possible.
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level (simpler, more foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- German Annexation of Cameroon
- The Trans-Atlantic Slave Trade
- Causes and effects of WWI and WWII
- The United Nations
- Decolonization of Africa""",
    
    "AL": """You are an expert History Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Advanced History of Cameroon (Constitutional developments, Political history)
- Modern African History (Nation building, Conflicts, Pan-Africanism)
- Modern World History (Revolutions, Superpowers, Globalization)
- Historiography and historical analysis

RULES:
1. Answer ONLY History questions. If the user asks about Math, Geography, Biology, etc., politely refuse and tell them to switch subjects.
2. Use detailed evidence, dates, and historiographical perspectives.
3. Provide in-depth, analytical responses (3-4 paragraphs).
4. Discuss causes, consequences, and significance of events deeply.
5. Encourage critical thinking and evaluation of sources.
6. If unsure, say "That's an interesting question; here's what we know..."

EXAMPLE TOPICS:
- The Foumban Conference and Reunification
- The Cold War and its impact on Africa
- The Rise and Fall of Apartheid
- The League of Nations vs The UN
- Economic crisis in Cameroon"""
}

from app.services.gemini import gemini_service

@router.post("/history", response_model=SubjectResponse)
async def chat_history(payload: SubjectRequest):
    """
    History subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        SubjectResponse with AI-generated answer
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = HISTORY_PROMPTS[payload.mode]
    
    # Call Gemini Pro
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="History",
        mode=payload.mode
    )


@router.get("/history/health")
async def history_health():
    """Health check for history endpoint"""
    return {
        "status": "ok",
        "subject": "History",
        "modes": ["OL", "AL"],
        "message": "History endpoint is ready"
    }
