import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    num_results: int = 5

@router.post("/research", summary="Perform a web search using SerpApi")
async def research(search_query: SearchQuery):
    """
    Perform a Google search using SerpApi and return structured results.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="SERPAPI_API_KEY not configured on server")

    try:
        params = {
            "engine": "google",
            "q": search_query.query,
            "api_key": api_key,
            "num": search_query.num_results
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
                "source": result.get("source")
            })

        return {
            "query": search_query.query,
            "results": formatted_results,
            "raw_metadata": results.get("search_metadata", {})
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
