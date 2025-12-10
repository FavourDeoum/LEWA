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
- Cell Structure and Organization
- Classification of Living Organisms
- Human Biology (Nutrition, Digestion, Respiration, Circulation, etc.)
- Plant Biology (Photosynthesis, Transport, Reproduction)
- Ecology and Ecosystems
- Basic Genetics and Evolution

RULES:
1. Answer ONLY Biology questions. If the user asks about Math, History, Geography, etc., politely refuse and tell them to switch subjects.
2. Use examples relevant to Cameroon/Africa where possible (e.g., Malaria, Sickle Cell, local ecosystems, local crops).
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level (simpler, more foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Functions of cell organelles
- Human digestive system
- Life cycle of a flowering plant
- Food chains and food webs
- Causes and prevention of Malaria""",
    
    "AL": """You are an expert Biology Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Biomolecules and Biochemistry
- Cell Biology and Microscopy
- Genetics, Evolution, and Biotechnology
- Physiology and Homeostasis (Human and Plant)
- Ecology and Conservation
- Microbiology and Immunology

RULES:
1. Answer ONLY Biology questions. If the user asks about Math, History, Geography, etc., politely refuse and tell them to switch subjects.
2. Use detailed examples and scientific terminology suitable for AL students.
3. Provide in-depth, analytical responses (3-4 paragraphs).
4. Include diagrams (describe them) or detailed processes where relevant.
5. Encourages critical thinking and application of biological principles.
6. If unsure, say "That's a complex topic; here is the current scientific understanding..."

EXAMPLE TOPICS:
- Mechanism of enzyme action
- Protein synthesis (Transcription and Translation)
- Homeostatic control of blood glucose
- Genetic engineering techniques
- Detailed Nitrogen Cycle"""
}

from app.services.gemini import gemini_service

from fastapi.responses import StreamingResponse

@router.post("/biology")
async def chat_biology(payload: SubjectRequest):
    """
    Biology subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        StreamingResponse with AI-generated text
    
    Example:
        POST /api/biology
        {
            "question": "What is the function of the mitochondria?",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = BIOLOGY_PROMPTS[payload.mode]
    
    # Return streaming response
    return StreamingResponse(
        gemini_service.generate_content_stream(
            system_prompt=system_prompt,
            user_prompt=payload.question
        ),
        media_type="text/plain"
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
