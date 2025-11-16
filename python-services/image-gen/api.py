"""Image generation service API endpoints."""
from fastapi import APIRouter, HTTPException
from common.models import ImageGenerationRequest, TemplateImageRequest
from common.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/generate")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate branded image.

    Args:
        request: Image generation request

    Returns:
        Generated image information
    """
    # TODO: Implement image generation
    logger.info(f"Image generation requested for project: {request.project_id}")

    return {
        "status": "not_implemented",
        "message": "Image generation not yet implemented"
    }


@router.post("/from-template")
async def generate_from_template(request: TemplateImageRequest):
    """
    Generate image using predefined template.

    Args:
        request: Template-based image request

    Returns:
        Generated image information
    """
    # TODO: Implement template-based generation
    logger.info(f"Template image requested for project: {request.project_id}")

    return {
        "status": "not_implemented",
        "message": "Template image generation not yet implemented"
    }


@router.get("/styles")
async def get_available_styles():
    """
    List available style presets.

    Returns:
        Available styles
    """
    return {
        "styles": ["social_media", "infographic", "announcement"],
        "templates": ["twitter_announcement", "feature_highlight", "infographic", "comparison", "announcement"]
    }
