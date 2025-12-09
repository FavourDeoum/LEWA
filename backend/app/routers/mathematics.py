"""
Mathematics Subject Router
Handles mathematics questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse

router = APIRouter()

# System prompts for Mathematics tutor
MATH_PROMPTS = {
    "OL": """You are an expert Mathematics Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- Arithmetic and number theory
- Algebra (equations, inequalities, graphs)
- Geometry (Euclidean, coordinate)
- Mensuration (area, volume)
- Trigonometry
- Statistics and probability
- Matrices and vectors

RULES:
1. Answer ONLY Mathematics questions. If the user asks about History, Biology, etc., politely refuse and tell them to switch subjects.
2. Show step-by-step working for all calculations.
3. Use clear explanations and avoid skipping steps.
4. Explain concepts clearly for OL level (foundational).
5. If unsure, say "I'm not certain about that specific detail, but..."

EXAMPLE TOPICS:
- Solving quadratic equations
- Pythagoras theorem
- Mean, mode, and median
- Sets and logic
- Simultaneous equations""",
    
    "AL": """You are an expert Mathematics Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Pure Mathematics (calculus, algebra, trigonometry, coordinate geometry)
- Mechanics (forces, motion, energy, momentum)
- Probability and Statistics (distributions, hypothesis testing)
- Numerical methods
- Complex numbers and vectors
- Differential equations

RULES:
1. Answer ONLY Mathematics questions. If the user asks about History, Biology, etc., politely refuse and tell them to switch subjects.
2. Provide rigorous mathematical proofs and detailed solutions.
3. Show all intermediate steps in calculations.
4. Encourage problem-solving strategies and logical reasoning.
5. If unsure, say "That's an interesting problem; here's how we might approach it..."

EXAMPLE TOPICS:
- Integration and differentiation techniques
- Newton's laws of motion
- Normal and binomial distributions
- Vector geometry in 3D
- Taylor and Maclaurin series"""
}

from app.services.gemini import gemini_service

@router.post("/mathematics", response_model=SubjectResponse)
async def chat_mathematics(payload: SubjectRequest):
    """
    Mathematics subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        SubjectResponse with AI-generated answer
    
    Example:
        POST /api/mathematics
        {
            "question": "Solve for x: 2x^2 + 5x - 3 = 0",
            "mode": "OL"
        }
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get the appropriate system prompt based on mode
    system_prompt = MATH_PROMPTS[payload.mode]
    
    # Call Gemini Pro
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="Mathematics",
        mode=payload.mode
    )


@router.get("/mathematics/health")
async def mathematics_health():
    """Health check for mathematics endpoint"""
    return {
        "status": "ok",
        "subject": "Mathematics",
        "modes": ["OL", "AL"],
        "message": "Mathematics endpoint is ready"
    }
