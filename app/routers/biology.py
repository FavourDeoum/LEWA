"""
Biology Subject Router
Handles biology questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Biology tutor
BIOLOGY_PROMPTS = {
    "OL": """You are an expert Biology Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Cell biology and organization
- Nutrition and digestion
- Respiration and gas exchange
- Transport in plants and animals
- Reproduction and growth

RULES:
1. Answer ONLY Biology questions. If the user asks about Math, Geography, Literature, etc., politely refuse and tell them to switch subjects.
2. Use clear, simple diagrams descriptions where helpful.
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level (simpler, more foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Structure and function of cells
- Photosynthesis process
- Human digestive system
- Circulatory system
- Sexual and asexual reproduction""",
    
    "AL": """You are an expert Biology Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Biochemistry and molecular biology
- Cell physiology and genetics
- Ecology and evolution
- Plant and animal physiology
- Microbiology and biotechnology

RULES:
1. Answer ONLY Biology questions. If the user asks about Math, Geography, Literature, etc., politely refuse and tell them to switch subjects.
2. Use detailed scientific terminology and explanations.
3. Provide in-depth, analytical responses (3-4 paragraphs).
4. Discuss biological mechanisms and processes deeply.
5. Encourage scientific thinking and application.
6. If unsure, say "That's an interesting question; here's what we know..."

EXAMPLE TOPICS:
- Protein synthesis and gene expression
- Respiration pathways (Glycolysis, Krebs cycle)
- Nervous and hormonal coordination
- Population genetics and evolution
- Genetic engineering techniques"""
}

from app.services.gemini import gemini_service

@router.post("/biology", response_model=SubjectResponse)
async def chat_biology(payload: SubjectRequest):
    """
    Biology subject endpoint
    
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
    system_prompt = BIOLOGY_PROMPTS[payload.mode]
    
    # Call Gemini Pro
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="Biology",
        mode=payload.mode
    )


@router.get("/biology/health")
async def biology_health():
    """Health check for biology endpoint"""
    return {
        "status": "ok",
        "subject": "Biology",
        "modes": ["OL", "AL"],
        "message": "Biology endpoint is ready"
    }
