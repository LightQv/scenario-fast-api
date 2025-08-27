from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.core.middleware import setup_cors
from app.core.settings import settings
from app.api.v1.router import main_router

# Créer l'application FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Configuration CORS
setup_cors(app=app)

# Inclure les routes API
app.include_router(main_router, prefix="/api/v1")

# Exception handlers
register_exception_handlers(app)

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