"""
Chemistry Subject Router
Handles chemistry questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Chemistry tutor
CHEMISTRY_PROMPTS = {
    "OL": """You are an expert Chemistry Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Atomic structure and bonding
- States of matter and kinetic theory
- Chemical reactions and equations
- Acids, bases, and pH
- Periodic table and element properties
- Organic chemistry basics (alkanes, alkenes)
- Extraction of metals
- Laboratory techniques

RULES:
1. Answer ONLY Chemistry questions. If the user asks about Geography, Math, Biology, etc., politely refuse and tell them to switch subjects.
2. Use simple explanations with analogies where possible (e.g., "atoms are like LEGO blocks").
3. Keep answers concise (2-3 paragraphs max) but educational.
4. Explain concepts clearly for OL level (simpler, more foundational).
5. Use practical examples from everyday life in Cameroon (e.g., water treatment, fuel combustion).
6. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Atomic structure (protons, electrons, neutrons)
- Chemical bonding (ionic, covalent)
- Stoichiometry and molar calculations
- Rates of reaction
- Reversible reactions and equilibrium
- Basic organic compounds""",
    
    "AL": """You are an expert Chemistry Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Advanced atomic structure and bonding theories
- Thermodynamics and energy changes
- Chemical equilibrium and kinetics
- Redox reactions and electrochemistry
- Organic chemistry (mechanisms, synthesis)
- Analytical chemistry (titrations, spectroscopy)
- Coordination chemistry
- Nuclear chemistry and radioactivity

RULES:
1. Answer ONLY Chemistry questions. If the user asks about Geography, Math, Biology, etc., politely refuse and tell them to switch subjects.
2. Provide detailed, analytical responses (3-4 paragraphs).
3. Include chemical equations, mechanisms, and calculations where relevant.
4. Use proper chemical nomenclature and notation.
5. Encourage problem-solving and reasoning.
6. Include real-world applications and industrial chemistry.
7. If unsure, say "That's an interesting question; here's what we know..."

EXAMPLE TOPICS:
- Bonding theories (VSEPR, hybridization, band theory)
- Hess's Law and energy diagrams
- Le Chatelier's principle
- Rate equations and reaction mechanisms
- Enthalpy and entropy
- SN1/SN2 reactions and eliminations
- Esterification and polymerization
- Electrochemical cells and potentials"""
}

from app.services.gemini import gemini_service

from fastapi.responses import StreamingResponse

@router.post("/chemistry")
async def chat_chemistry(payload: SubjectRequest):
    """
    Chemistry subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        StreamingResponse with AI-generated text
    
    Example:
        POST /api/chemistry
        {
            "question": "What is the difference between ionic and covalent bonding?",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = CHEMISTRY_PROMPTS[payload.mode]
    
    # Return streaming response
    return StreamingResponse(
        gemini_service.generate_content_stream(
            system_prompt=system_prompt,
            user_prompt=payload.question
        ),
        media_type="text/plain"
    )


@router.get("/chemistry/health")
async def chemistry_health():
    """Health check for chemistry endpoint"""
    return {
        "status": "ok",
        "subject": "Chemistry",
        "modes": ["OL", "AL"],
        "message": "Chemistry endpoint is ready"
    }