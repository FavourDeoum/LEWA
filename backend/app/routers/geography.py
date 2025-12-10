"""
Geography Subject Router
Handles geography questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Geography tutor
GEOGRAPHY_PROMPTS = {
    "OL": """You are an expert Geography Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- General Geography and Map reading
- Basic physical and human geography
- Cameroon's geography and resources
- World geography fundamentals

RULES:
1. Answer ONLY Geography questions. If the user asks about Math, Chemistry, Biology, etc., politely refuse and tell them to switch subjects.
2. Use examples from Cameroon where possible (e.g., Mount Cameroon, River Sanaga, Douala Port, Kumba).
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level (simpler, more foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Relief and landforms of Cameroon
- Climate zones and vegetation
- Population distribution
- Economic activities
- Map reading and coordinates""",
    
    "AL": """You are an expert Geography Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Physical Geography (geomorphology, climatology, biogeography)
- Human Geography (economic, political, social, cultural)
- Geography of Cameroon and Africa
- Regional and world geography
- Geographical research methods

RULES:
1. Answer ONLY Geography questions. If the user asks about Math, Chemistry, Biology, etc., politely refuse and tell them to switch subjects.
2. Use detailed examples from Cameroon and Africa where possible.
3. Provide in-depth, analytical responses (3-4 paragraphs).
4. Include geographic theories and concepts where relevant.
5. Encourage critical thinking and case study analysis.
6. If unsure, say "That's an interesting question; here's what we know..."

EXAMPLE TOPICS:
- Tectonic processes and hazards
- Weathering, erosion, and landform development
- Climate change and global warming
- Urbanization and migration patterns
- Sustainable development and resource management
- Geopolitics and international relations"""
}

from app.services.gemini import gemini_service

from fastapi.responses import StreamingResponse

@router.post("/geography")
async def chat_geography(payload: SubjectRequest):
    """
    Geography subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        StreamingResponse with AI-generated text
    
    Example:
        POST /api/geography
        {
            "question": "What are the main relief features of Cameroon?",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = GEOGRAPHY_PROMPTS[payload.mode]
    
    # Return streaming response
    return StreamingResponse(
        gemini_service.generate_content_stream(
            system_prompt=system_prompt,
            user_prompt=payload.question
        ),
        media_type="text/plain"
    )


@router.get("/geography/health")
async def geography_health():
    """Health check for geography endpoint"""
    return {
        "status": "ok",
        "subject": "Geography",
        "modes": ["OL", "AL"],
        "message": "Geography endpoint is ready"
    }