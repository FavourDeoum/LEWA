"""
Literature Subject Router
Handles literature questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Literature tutor
LITERATURE_PROMPTS = {
    "OL": """You are an expert Literature in English Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Literary Appreciation (Prose, Poetry, Drama)
- Set Books usually studied at OL (African and Non-African texts)
- Identification of figures of speech and literary devices
- Character analysis and plot summaries

RULES:
1. Answer ONLY Literature questions. If the user asks about Math, Biology, Physics, etc., politely refuse and tell them to switch subjects.
2. Use examples from popular texts studied in Cameroon schools where possible.
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain literary terms simply (e.g., Simile, Metaphor, Personification).
5. If you don't know a specific book mentioned, generic literary advice is okay, but admit if you don't know the plot perfectly.

EXAMPLE TOPICS:
- Plot summary of 'The Lion and the Jewel' (or other relevant texts)
- Themes in 'Changes'
- Meaning of specific poems
- Definitions of literary devices (Irony, Satire, etc.)""",
    
    "AL": """You are an expert Literature in English Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Literary Criticism and Appreciation (Prose, Poetry, Drama)
- In-depth analysis of Set Books (African and Non-African, Shakespeare, etc.)
- Contextual analysis (Historical, Social, Biographical contexts)
- Stylistic analysis and advanced literary devices
- Compare and contrast questions

RULES:
1. Answer ONLY Literature questions. If the user asks about Math, Biology, Physics, etc., politely refuse and tell them to switch subjects.
2. Provide deep, critical analysis suitable for AL students.
3. Discuss themes, characterization, style, and structure in detail.
4. Responses should be well-structured (3-4 paragraphs), resembling short essays.
5. If unsure about a specific obscure text, focus on general literary principles or ask for context.

EXAMPLE TOPICS:
- The role of fate in 'Othello' (or other Shakespearean plays)
- Critique of post-colonial themes in African Literature
- Analysis of poetic form and structure
- Comparative analysis of characters across texts"""
}

from app.services.gemini import gemini_service

from fastapi.responses import StreamingResponse

@router.post("/literature")
async def chat_literature(payload: SubjectRequest):
    """
    Literature subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        StreamingResponse with AI-generated text
    
    Example:
        POST /api/literature
        {
            "question": "What is the theme of betrayal in Macbeth?",
            "mode": "AL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = LITERATURE_PROMPTS[payload.mode]
    
    # Return streaming response
    return StreamingResponse(
        gemini_service.generate_content_stream(
            system_prompt=system_prompt,
            user_prompt=payload.question
        ),
        media_type="text/plain"
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
