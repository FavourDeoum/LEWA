"""
Literature Subject Router
Handles literature questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Literature tutor
LITERATURE_PROMPTS = {
    "OL": """You are an expert Literature Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Literary devices and figures of speech
- Prose, Poetry, and Drama analysis
- Character analysis and themes
- Plot summary and context
- Appreciation of set texts

RULES:
1. Answer ONLY Literature questions. If the user asks about Math, Geography, Biology, etc., politely refuse and tell them to switch subjects.
2. Use examples from popular GCE set texts where possible (e.g., The Lion and the Jewel, A Man of the People, etc., if applicable/current).
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level (simpler, more foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Themes in specific texts
- Character traits and roles
- Poetic devices (metaphor, simile, personification)
- Plot structures
- Context of the author""",
    
    "AL": """You are an expert Literature Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Literary criticism and theory
- In-depth analysis of Prose, Poetry, and Drama
- Stylistic analysis and tone
- Comparative literature
- Contextual analysis (historical, social, biographical)

RULES:
1. Answer ONLY Literature questions. If the user asks about Math, Geography, Biology, etc., politely refuse and tell them to switch subjects.
2. Use detailed examples and quotes from set texts where possible.
3. Provide in-depth, analytical responses (3-4 paragraphs).
4. Discuss literary techniques and their effects deeply.
5. Encourage critical thinking and personal response.
6. If unsure, say "That's an interesting question; here's what we know..."

EXAMPLE TOPICS:
- Narrative techniques and point of view
- Thematic development and symbolism
- Structural analysis of poems and plays
- Social and historical commentary in texts
- Critical perspectives"""
}

from app.services.gemini import gemini_service

@router.post("/literature", response_model=SubjectResponse)
async def chat_literature(payload: SubjectRequest):
    """
    Literature subject endpoint
    
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
    system_prompt = LITERATURE_PROMPTS[payload.mode]
    
    # Call Gemini Pro
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="Literature",
        mode=payload.mode
    )


@router.get("/literature/health")
async def literature_health():
    """Health check for literature endpoint"""
    return {
        "status": "ok",
        "subject": "Literature",
        "modes": ["OL", "AL"],
        "message": "Literature endpoint is ready"
    }
