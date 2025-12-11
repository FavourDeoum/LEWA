"""
Messenger Router
Handles announcements, exam notices, and notifications for GCE Board updates
"""
import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from serpapi import GoogleSearch
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter()

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class AnnouncementRequest(BaseModel):
    """Request for GCE announcements"""
    subject: Optional[str] = None  # Filter by subject (optional)
    include_exam_dates: bool = True
    include_resources: bool = True

class ExamNoticeRequest(BaseModel):
    """Request for exam notices"""
    query: str  # Custom search query for exam notices
    num_results: int = 5
    include_cameroon: bool = True  # Focus on Cameroon updates

class NotificationRequest(BaseModel):
    """Request for smart notifications"""
    keywords: List[str]  # Keywords to monitor (e.g., ["exam date", "results", "registration"])
    subjects: Optional[List[str]] = None  # Subjects to monitor

class AnnouncementResponse(BaseModel):
    """Response containing announcements"""
    timestamp: str
    announcements: List[dict]
    exam_dates: Optional[List[dict]] = None
    resources: Optional[List[dict]] = None

class ExamNoticeResponse(BaseModel):
    """Response containing exam notices"""
    query: str
    timestamp: str
    notices: List[dict]
    source: str

class NotificationResponse(BaseModel):
    """Response containing smart notifications"""
    timestamp: str
    keywords: List[str]
    notifications: List[dict]
    alert_level: str  # "high", "medium", "low"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def search_gce_announcements(subject: Optional[str] = None) -> List[dict]:
    """
    Search for GCE Board announcements
    
    Args:
        subject: Optional subject filter
    
    Returns:
        List of announcements
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="SERPAPI_API_KEY not configured")

    try:
        # Construct search query
        search_term = "GCE Cameroon announcements 2024 2025"
        if subject:
            search_term += f" {subject}"
        
        params = {
            "engine": "google",
            "q": search_term,
            "api_key": api_key,
            "num": 10,
            "tbm": "nws"  # News search
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=f"Search error: {results['error']}")
        
        announcements = []
        news_results = results.get("news_results", [])
        
        for item in news_results:
            announcements.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "source": item.get("source"),
                "date": item.get("date"),
                "snippet": item.get("snippet")
            })
        
        return announcements
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching announcements: {str(e)}")


async def search_exam_notices(query: str, include_cameroon: bool = True) -> List[dict]:
    """
    Search for exam notices and updates
    
    Args:
        query: Search query for exam notices
        include_cameroon: Whether to focus on Cameroon-specific results
    
    Returns:
        List of exam notices
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="SERPAPI_API_KEY not configured")

    try:
        search_term = query
        if include_cameroon:
            search_term += " Cameroon GCE"
        
        params = {
            "engine": "google",
            "q": search_term,
            "api_key": api_key,
            "num": 10,
            "tbm": "nws"  # News search
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=f"Search error: {results['error']}")
        
        notices = []
        news_results = results.get("news_results", [])
        
        for item in news_results:
            notices.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "source": item.get("source"),
                "date": item.get("date"),
                "snippet": item.get("snippet")
            })
        
        return notices
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exam notices: {str(e)}")


def generate_smart_notifications(keywords: List[str], subjects: Optional[List[str]] = None) -> List[dict]:
    """
    Generate smart notifications based on keywords and subjects
    
    Args:
        keywords: Keywords to monitor
        subjects: Subjects to monitor
    
    Returns:
        List of smart notifications
    """
    notifications = []
    
    # Generate notifications based on keywords
    notification_templates = {
        "exam date": {
            "icon": "📅",
            "priority": "high",
            "message": "New exam date announcement detected. Check your subject schedule."
        },
        "results": {
            "icon": "📊",
            "priority": "high",
            "message": "Result notification found. Your exam results may be available."
        },
        "registration": {
            "icon": "📝",
            "priority": "high",
            "message": "Registration deadline detected. Complete your registration immediately."
        },
        "postponed": {
            "icon": "⏸️",
            "priority": "high",
            "message": "Exam postponement notice detected. Check the details carefully."
        },
        "update": {
            "icon": "🔔",
            "priority": "medium",
            "message": "GCE Board update available. Review the latest information."
        },
        "deadline": {
            "icon": "⚠️",
            "priority": "high",
            "message": "Important deadline approaching. Take action now."
        }
    }
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        for template_key, template in notification_templates.items():
            if template_key in keyword_lower:
                notification = {
                    "keyword": keyword,
                    "icon": template["icon"],
                    "priority": template["priority"],
                    "message": template["message"],
                    "timestamp": datetime.now().isoformat()
                }
                
                # Add subject-specific info if subjects provided
                if subjects:
                    notification["subjects"] = subjects
                
                notifications.append(notification)
    
    return notifications


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/messenger/announcements", response_model=AnnouncementResponse, summary="Get GCE Announcements")
async def get_announcements(request: AnnouncementRequest):
    """
    Fetch GCE Board announcements and updates
    
    Args:
        request: AnnouncementRequest with optional subject filter
    
    Returns:
        AnnouncementResponse with fetched announcements
    
    Example:
        POST /api/messenger/announcements
        {
            "subject": "Mathematics",
            "include_exam_dates": true,
            "include_resources": true
        }
    """
    try:
        announcements = await search_gce_announcements(request.subject)
        
        exam_dates = None
        resources = None
        
        if request.include_exam_dates:
            exam_dates = [
                {
                    "level": "OL",
                    "period": "June 2024",
                    "status": "Completed"
                },
                {
                    "level": "AL",
                    "period": "June 2024",
                    "status": "Completed"
                },
                {
                    "level": "OL",
                    "period": "December 2024",
                    "status": "Completed"
                },
                {
                    "level": "AL",
                    "period": "December 2024",
                    "status": "In Progress or Upcoming"
                }
            ]
        
        if request.include_resources:
            resources = [
                {
                    "title": "GCE Official Website",
                    "url": "https://www.gce.cm",
                    "type": "Official"
                },
                {
                    "title": "Cameroon's National Examination Board",
                    "url": "https://www.minedub.cm",
                    "type": "Government"
                }
            ]
        
        return AnnouncementResponse(
            timestamp=datetime.now().isoformat(),
            announcements=announcements,
            exam_dates=exam_dates,
            resources=resources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving announcements: {str(e)}")


@router.post("/messenger/exam-notices", response_model=ExamNoticeResponse, summary="Get Exam Notices")
async def get_exam_notices(request: ExamNoticeRequest):
    """
    Search for latest exam notices and updates
    
    Args:
        request: ExamNoticeRequest with search query
    
    Returns:
        ExamNoticeResponse with exam notices
    
    Example:
        POST /api/messenger/exam-notices
        {
            "query": "exam date 2024",
            "num_results": 5,
            "include_cameroon": true
        }
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        notices = await search_exam_notices(
            query=request.query,
            include_cameroon=request.include_cameroon
        )
        
        return ExamNoticeResponse(
            query=request.query,
            timestamp=datetime.now().isoformat(),
            notices=notices,
            source="GCE Board & News"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving exam notices: {str(e)}")


@router.post("/messenger/notifications", response_model=NotificationResponse, summary="Get Smart Notifications")
async def get_notifications(request: NotificationRequest):
    """
    Generate smart notifications based on keywords and subjects
    
    Args:
        request: NotificationRequest with keywords and subjects
    
    Returns:
        NotificationResponse with smart notifications
    
    Example:
        POST /api/messenger/notifications
        {
            "keywords": ["exam date", "results", "registration"],
            "subjects": ["Mathematics", "English"]
        }
    """
    try:
        if not request.keywords or len(request.keywords) == 0:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        
        notifications = generate_smart_notifications(
            keywords=request.keywords,
            subjects=request.subjects
        )
        
        # Determine alert level based on notification priorities
        high_priority_count = sum(1 for n in notifications if n.get("priority") == "high")
        
        if high_priority_count >= 3:
            alert_level = "high"
        elif high_priority_count >= 1:
            alert_level = "medium"
        else:
            alert_level = "low"
        
        return NotificationResponse(
            timestamp=datetime.now().isoformat(),
            keywords=request.keywords,
            notifications=notifications,
            alert_level=alert_level
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating notifications: {str(e)}")


@router.get("/messenger/health", summary="Health check for Messenger")
async def messenger_health():
    """Health check for messenger endpoint"""
    return {
        "status": "ok",
        "service": "Messenger",
        "features": [
            "GCE Announcements",
            "Exam Notices",
            "Smart Notifications"
        ],
        "message": "Messenger endpoint is ready"
    }
