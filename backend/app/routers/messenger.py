import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class MessengerQuery(BaseModel):
    query: str
    num_results: int = 5

@router.post("/messenger", summary="Get GCE Announcements")
async def get_gce_announcements(query_data: MessengerQuery):
    """
    Search for Cameroon GCE Board announcements using SerpApi.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="SERPAPI_API_KEY not configured on server")

    try:
        # bias search towards Cameroon GCE Board announcements
        search_term = f"Cameroon GCE Board announcements {query_data.query}".strip()
        
        params = {
            "engine": "google",
            "q": search_term,
            "api_key": api_key,
            "num": query_data.num_results,
            "tbs": "qdr:m" # limit to past month for relevance, or maybe remove strict time filter
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            raise HTTPException(status_code=500, detail=f"SerpApi error: {results['error']}")

        organic_results = results.get("organic_results", [])
        
        formatted_results = []
        for result in organic_results:
            formatted_results.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet"),
                "date": result.get("date", "Recent")
            })

        return {
            "query": search_term,
            "results": formatted_results,
            "topic": "GCE Announcements"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
