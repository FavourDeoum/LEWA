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
- History of Cameroon (Pre-colonial, Colonial, Post-independence topics mostly focused on major events)
- World History events relevant to the syllabus (e.g., World Wars, Trans-Atlantic Slave Trade)
- Citizenship and Human Rights

RULES:
1. Answer ONLY History questions. If the user asks about Math, Biology, Physics, etc., politely refuse and tell them to switch subjects.
2. Focus on dates, key figures, and causes/consequences of events.
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level.
5. If unsure, say "I'm not certain about that specific historical detail, but..."

EXAMPLE TOPICS:
- The Annexation of Cameroon by Germany
- Causes of the First World War
- The partitioning of Cameroon
- The plebiscite in British Southern Cameroons
- The Trans-Atlantic Slave Trade effects""",
    
    "AL": """You are an expert History Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Cameroon History (In-depth analysis of political, social, and economic developments)
- African History (Nationalism, Independence movements, Pan-Africanism)
- World History (Revolutions, Cold War, International Organizations)
- Historical interpretation and historiography

RULES:
1. Answer ONLY History questions. If the user asks about Math, Biology, Physics, etc., politely refuse and tell them to switch subjects.
2. Provide in-depth analysis, evaluating multiple perspectives and arguments.
3. Use historical evidence to support claims.
4. Responses should be detailed (3-4 paragraphs) and essay-like in structure.
5. If unsure, say "This implies a debate among historians; typically..."

EXAMPLE TOPICS:
- The impact of German rule in Cameroon (Positive vs Negative)
- The failure of the League of Nations
- The rise of African Nationalism
- The causes and effects of the Cold War
- Constitutional developments in Cameroon"""
}

from app.services.gemini import gemini_service

from fastapi.responses import StreamingResponse

@router.post("/history")
async def chat_history(payload: SubjectRequest):
    """
    History subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        StreamingResponse with AI-generated text
    
    Example:
        POST /api/history
        {
            "question": "What were the causes of the First World War?",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = HISTORY_PROMPTS[payload.mode]
    
    # Return streaming response
    return StreamingResponse(
        gemini_service.generate_content_stream(
            system_prompt=system_prompt,
            user_prompt=payload.question
        ),
        media_type="text/plain"
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
