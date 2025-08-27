from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.api.v1.router import api_router

# Créer l'application FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API pour l'application Scenario - Que regarder ce soir ?",
    debug=settings.debug
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url] + settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Inclure les routes API
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Point de départ de l'API."""
    return {
        "message": "Welcome to Scenario API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de vérification de santé."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=settings.debug
    )