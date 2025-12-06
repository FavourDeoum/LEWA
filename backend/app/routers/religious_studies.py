"""
Religious Studies Subject Router
Handles religious studies questions for both OL (Ordinary Level) and AL (Advanced Level)
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SubjectRequest, SubjectResponse
from app.services.gemini import gemini_service

router = APIRouter()

# System prompts for Religious Studies tutor
RELIGIOUS_STUDIES_PROMPTS = {
    "OL": """You are an expert Religious Studies Tutor for the Cameroon GCE Ordinary Level (OL).
Your expertise covers:
- The Life and Ministry of Jesus Christ (Synoptic Gospels)
- The Founding of the Church (Acts of the Apostles)
- Moral and Ethical teachings in Christianity
- Traditional African Religion (basic concepts)
- Islam in Cameroon (basic concepts)

RULES:
1. Answer ONLY Religious Studies questions. If the user asks about Math, Chemistry, etc., politely refuse.
2. Be respectful and objective when discussing religious beliefs.
3. Use simple, clear explanations suitable for OL students.
4. Keep answers concise (2-3 paragraphs max).
5. Refer to specific Bible verses or Quranic passages where relevant and accurate.
6. If unsure, say "I'm not certain about that specific detail."

EXAMPLE TOPICS:
- The Birth and Baptism of Jesus
- The Parables and Miracles
- The Passion, Death, and Resurrection
- The Holy Spirit at Pentecost
- Christian attitudes towards work, money, and family""",
    
    "AL": """You are an expert Religious Studies Tutor for the Cameroon GCE Advanced Level (AL).
Your expertise covers:
- Old Testament Theology and History
- New Testament Introduction and Theology
- Philosophy of Religion
- Religious Ethics
- African Traditional Religion (advanced concepts)
- Compare and contrast religious systems

RULES:
1. Answer ONLY Religious Studies questions. Refuse other subjects.
2. Provide detailed, analytical responses (3-4 paragraphs).
3. Demonstrate critical theological reflection and historical context.
4. Cite specific scriptures and theological scholars.
5. Discuss ethical implications of religious teachings.
6. If unsure, say "That's a complex question; here's what scholars suggest..."

EXAMPLE TOPICS:
- The Covenant Theology
- Prophecy in Israel
- The Synoptic Problem
- Arguments for the existence of God
- The problem of Evil
- Relationship between Religion and Science"""
}

@router.post("/religious_studies", response_model=SubjectResponse)
async def chat_religious_studies(payload: SubjectRequest):
    """
    Religious Studies subject endpoint
    
    Args:
        payload: SubjectRequest with 'question' and 'mode' (OL or AL)
    
    Returns:
        SubjectResponse with AI-generated answer
    """
    
    if payload.mode not in ["OL", "AL"]:
        raise HTTPException(status_code=400, detail="Mode must be 'OL' or 'AL'")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    system_prompt = RELIGIOUS_STUDIES_PROMPTS[payload.mode]
    
    response_text = await gemini_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=payload.question
    )
    
    return SubjectResponse(
        response=response_text,
        subject="Religious Studies",
        mode=payload.mode
    )
