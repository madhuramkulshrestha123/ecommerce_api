from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from typing import Dict, Any
import time

from core.database import get_database


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: str
    version: str
    timestamp: float
    database: Dict[str, Any]


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health of the API and its dependencies."
)
async def health_check(db = Depends(get_database)):
    """
    Perform a health check of the API and its dependencies.
    
    Checks:
    - API availability
    - Database connection
    
    Returns a status report with timestamp and version information.
    """
    # Check database connection
    db_status = {"status": "healthy"}
    try:
        # Simple ping to check database connection
        await db.command("ping")
    except Exception as e:
        db_status = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Get API version from settings
    from core.config import settings
    
    return HealthResponse(
        status="healthy" if db_status["status"] == "healthy" else "degraded",
        version=settings.PROJECT_VERSION,
        timestamp=time.time(),
        database=db_status
    ) 