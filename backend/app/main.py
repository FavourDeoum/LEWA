from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from app.routers import chemistry, economics, geography, religious_studies, french, research

app = FastAPI(
    title="LEWA - AI Tutor",
    description="AI-powered educational assistant for GCE OL & AL students",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "LEWA Backend"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to LEWA - AI Tutor API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "geography": "/api/geography",
            "chemistry": "/api/chemistry",
            "economics": "/api/economics",
            "religious_studies": "/api/religious_studies",
            "french": "/api/french"
        }
    }

# Include subject routers
app.include_router(geography.router, prefix="/api", tags=["Geography"])
app.include_router(chemistry.router, prefix="/api", tags=["Chemistry"])
app.include_router(economics.router, prefix="/api", tags=["Economics"])
app.include_router(religious_studies.router, prefix="/api", tags=["Religious Studies"])
app.include_router(french.router, prefix="/api", tags=["French"])
app.include_router(research.router, prefix="/api", tags=["Research"])