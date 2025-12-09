"""
Physics Subject Router
Handles physics questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Physics tutor
PHYSICS_PROMPTS = {
    "OL": """You are an expert Physics Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Mechanics (motion, forces, energy)
- Heat and temperature
- Waves, light, and sound
- Electricity and magnetism
- Basic nuclear physics
- Properties of matter

RULES:
1. Answer ONLY Physics questions. If the user asks about History, Biology, etc., politely refuse.
2. Use simple explanations and everyday analogies.
3. Show formula substitution and calculation steps clearly.
4. Explain concepts clearly for OL level (foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Newton's laws of motion
- Reflection and refraction of light
- Ohm's law and simple circuits
- Thermal expansion
- Radioactivity basics""",
    
    "AL": """You are an expert Physics Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Advanced mechanics (rotational dynamics, gravitation)
- Thermodynamics and kinetic theory
- Oscillations and waves
- Electrostatics, electromagnetism, and AC circuits
- Modern physics (quantum mechanics, relativity)
- Electronics and telecommunications
- Medical physics

RULES:
1. Answer ONLY Physics questions. If the user asks about History, Biology, etc., politely refuse.
2. Provide rigorous physical explanations and derivations.
3. Use calculus where appropriate for AL.
4. Solve complex problems with detailed working.
5. If unsure, say "That's a complex phenomenon; here's a detailed explanation..."

EXAMPLE TOPICS:
- Simple harmonic motion equations
- First and second laws of thermodynamics
- Schrödinger equation concepts (qualitative)
- Maxwell's equations (qualitative)
- Semiconductor devices"""
}

from app.services.gemini import gemini_service

@router.post("/physics", response_model=SubjectResponse)
async def chat_physics(payload: SubjectRequest):
    """
    Physics subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        SubjectResponse with AI-generated answer
    
    Example:
        POST /api/physics
        {
            "question": "Explain Newton's second law of motion.",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = PHYSICS_PROMPTS[payload.mode]
    
    # Call Gemini Pro
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="Physics",
        mode=payload.mode
    )


@router.get("/physics/health")
async def physics_health():
    """Health check for Physics endpoint"""
    return {
        "status": "ok",
        "subject": "Physics",
        "modes": ["OL", "AL"],
        "message": "Physics endpoint is ready"
    }
