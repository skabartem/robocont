"""Research service API endpoints."""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from common.models import ProjectResearchRequest, ProjectResearchResponse
from common.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/start", response_model=ProjectResearchResponse)
async def start_research(request: ProjectResearchRequest, background_tasks: BackgroundTasks):
    """
    Start research on a new project.

    Returns:
        ProjectResearchResponse with project_id and status
    """
    # TODO: Implement research logic
    logger.info(f"Research requested for: {request.url}")

    return {
        "project_id": "placeholder",
        "status": "not_implemented",
        "progress": 0,
        "data": None
    }


@router.get("/status/{project_id}", response_model=ProjectResearchResponse)
async def get_research_status(project_id: str):
    """
    Check research progress.

    Args:
        project_id: Project identifier

    Returns:
        Research status and data
    """
    # TODO: Implement status checking
    return {
        "project_id": project_id,
        "status": "not_implemented",
        "progress": 0,
        "data": None
    }


@router.get("/project/{project_id}")
async def get_project_data(project_id: str):
    """
    Retrieve complete project research data.

    Args:
        project_id: Project identifier

    Returns:
        Complete research data
    """
    # TODO: Implement data retrieval
    return {
        "project_id": project_id,
        "message": "Data retrieval not yet implemented"
    }
