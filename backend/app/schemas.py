from pydantic import BaseModel
from typing import Literal

class SubjectRequest(BaseModel):
    """Request body for subject-specific chat endpoints"""
    question: str
    mode: Literal["OL", "AL"]  # Ordinary Level or Advanced Level

class SubjectResponse(BaseModel):
    """Response from subject-specific chat endpoints"""
    response: str
    subject: str
    mode: Literal["OL", "AL"]
    
class ErrorResponse(BaseModel):
    """Error response structure"""
    error: str
    detail: str