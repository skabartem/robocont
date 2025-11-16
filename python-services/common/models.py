"""Pydantic models for request/response validation."""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict
from datetime import datetime


# Request Models
class ProjectResearchRequest(BaseModel):
    """Request model for project research."""
    url: HttpUrl
    contract_address: Optional[str] = None
    include_social: bool = True


class TwitterPostRequest(BaseModel):
    """Request model for Twitter post generation."""
    project_id: str
    type: str = Field(..., pattern="^(announcement|feature|update|education)$")
    key_point: Optional[str] = None


class TwitterThreadRequest(BaseModel):
    """Request model for Twitter thread generation."""
    project_id: str
    topic: str
    num_tweets: int = 7


class DescriptionRequest(BaseModel):
    """Request model for project description generation."""
    project_id: str
    length: str = Field(default="medium", pattern="^(short|medium|long)$")


class FeatureRequest(BaseModel):
    """Request model for feature explanation generation."""
    project_id: str
    feature_name: str
    audience: str = Field(default="general", pattern="^(general|technical|investor)$")


class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""
    project_id: str
    template: str
    variables: Dict[str, str]
    custom_prompt: Optional[str] = None


class TemplateImageRequest(BaseModel):
    """Request model for template-based image generation."""
    project_id: str
    template_name: str
    variables: Dict[str, str]


class BatchImageRequest(BaseModel):
    """Request model for batch image generation."""
    project_id: str
    templates: List[Dict[str, any]]


class ScriptGenerationRequest(BaseModel):
    """Request model for video script generation."""
    project_id: str
    video_type: str = Field(..., pattern="^(intro|feature|tutorial)$")
    duration: int = 30
    custom_requirements: Optional[str] = None


class VideoGenerationRequest(BaseModel):
    """Request model for video generation."""
    script_id: str
    scene_numbers: Optional[List[int]] = None
    style: Optional[str] = None


class BlogPostRequest(BaseModel):
    """Request model for blog post generation."""
    project_id: str
    topic: str
    word_count: int = 1000


# Response Models
class ProjectResearchResponse(BaseModel):
    """Response model for project research."""
    project_id: str
    status: str
    progress: int = Field(..., ge=0, le=100)
    data: Optional[Dict] = None


class TwitterPostResponse(BaseModel):
    """Response model for Twitter post."""
    text: str
    hashtags: List[str]
    character_count: int
    suggested_image: Optional[str] = None


class GenerationStatusResponse(BaseModel):
    """Response model for generation status."""
    generation_id: str
    status: str
    progress: int
    result_url: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str


class APIRootResponse(BaseModel):
    """Response model for API root."""
    message: str
    version: str
    services: Dict[str, str]
