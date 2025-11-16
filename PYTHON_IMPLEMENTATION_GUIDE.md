# Python Implementation Guide - Crypto Content Automation

## Overview

This document provides detailed instructions for all Python components in the crypto content automation system. Python handles the AI-heavy operations while n8n orchestrates the workflows.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Python Services Architecture](#python-services-architecture)
3. [Research Service](#research-service)
4. [Text Generation Service](#text-generation-service)
5. [Image Generation Service](#image-generation-service)
6. [Video Generation Service](#video-generation-service)
7. [Common Utilities](#common-utilities)
8. [Database Management](#database-management)
9. [API Integration](#api-integration)
10. [Testing Strategy](#testing-strategy)

---

## Project Setup

### Directory Structure

```
python-services/
├── research/
│   ├── __init__.py
│   ├── ai_researcher.py    # AI-powered research (Perplexity/Tavily)
│   ├── analyzer.py         # Project analysis logic
│   ├── document_parser.py  # Parse PDFs, docs
│   └── api.py             # FastAPI endpoints
├── text-gen/
│   ├── __init__.py
│   ├── llm_client.py      # LLM API wrapper
│   ├── prompt_manager.py  # Prompt templates
│   ├── generators.py      # Content generators
│   └── api.py             # FastAPI endpoints
├── image-gen/
│   ├── __init__.py
│   ├── nano_banana.py     # Nano Banana API client
│   ├── style_manager.py   # Brand/mascot consistency
│   ├── templates.py       # Image templates
│   └── api.py             # FastAPI endpoints
├── video-gen/
│   ├── __init__.py
│   ├── veo_client.py      # VEO3.1 API client
│   ├── script_generator.py # Video script creation
│   ├── templates.py       # Video templates
│   └── api.py             # FastAPI endpoints
├── common/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── database.py        # SQLite operations
│   ├── models.py          # Pydantic models
│   ├── utils.py           # Helper functions
│   └── logger.py          # Logging setup
├── main.py                # Main FastAPI app
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Python services documentation
```

### Requirements.txt

```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0

# HTTP Clients
httpx==0.26.0
requests==2.31.0

# AI Research Services
tavily-python==0.3.0  # AI-powered research
# perplexityai==0.1.0  # Alternative research service (if available)

# Document Processing
pypdf2==3.0.1
python-docx==1.1.0
python-pptx==0.6.23

# LLM Integration
openai==1.10.0
anthropic==0.18.0
langchain==0.1.0
langchain-openai==0.0.5

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# Utilities
python-dotenv==1.0.0
tenacity==8.2.3  # Retry logic
validators==0.22.0

# Data Processing
pandas==2.2.0
numpy==1.26.3

# Social Media APIs
tweepy==4.14.0  # Twitter API (optional)

# Image Processing
pillow==10.2.0

# Testing
pytest==8.0.0
pytest-asyncio==0.23.3
httpx-mock==0.13.0
```

---

## Python Services Architecture

### Design Principles

1. **Microservices Pattern**: Each service is independent and communicates via APIs
2. **FastAPI for APIs**: Lightweight, async, auto-documentation
3. **Pydantic for Validation**: Type-safe data models
4. **Async/Await**: Non-blocking operations for better performance
5. **Environment-based Config**: Secure API key management
6. **Error Handling**: Comprehensive try-catch with retries
7. **Logging**: Structured logging for debugging

### Service Communication

```
n8n Workflow
    ↓ HTTP Request
FastAPI Endpoints (main.py)
    ↓ Route to Service
Individual Services
    ↓ Database
SQLite Storage
```

---

## Research Service

### Purpose
Gather and analyze information about crypto projects from various sources.

### Components

#### 1. AI Researcher (`ai_researcher.py`)

**Responsibilities:**
- Use AI research services to gather comprehensive project information
- Query multiple sources automatically
- Synthesize information from various sources
- Extract structured data about crypto projects

**Recommended Service: Tavily AI** (Best for this use case)
- Purpose-built for AI research tasks
- Cost-effective (~$0.005 per search)
- Deep research mode for comprehensive analysis
- Returns structured data with sources

**Alternative Services:**
- Perplexity AI (~$5 per 1000 searches, excellent quality)
- Exa AI (semantic search, good for finding specific content)

**Key Functions:**

```python
from tavily import TavilyClient
from typing import Optional, List
from tenacity import retry, stop_after_attempt

class AIResearcher:
    """AI-powered research using Tavily or Perplexity."""

    def __init__(self, api_key: str, service: str = "tavily"):
        """
        Initialize AI research client.

        Args:
            api_key: API key for research service
            service: 'tavily' or 'perplexity'
        """
        self.service = service
        if service == "tavily":
            self.client = TavilyClient(api_key=api_key)

    @retry(stop=stop_after_attempt(3))
    async def research_project(
        self,
        project_url: str,
        project_name: str = None,
        deep_research: bool = True
    ) -> dict:
        """
        Conduct comprehensive research on a crypto project.

        Args:
            project_url: Project website URL
            project_name: Project name (if known)
            deep_research: Use deep research mode for comprehensive analysis

        Returns:
            dict: {
                'summary': str,
                'description': str,
                'key_features': list,
                'tokenomics': dict,
                'technology': str,
                'team': list,
                'roadmap': list,
                'social_links': dict,
                'competitors': list,
                'sources': list (with URLs and snippets)
            }
        """
        # Build comprehensive research query
        query = self._build_research_query(project_url, project_name)

        # Perform research
        if self.service == "tavily":
            result = await self._tavily_research(query, deep_research)
        else:
            result = await self._perplexity_research(query)

        # Structure the research data
        structured_data = await self._structure_research_results(result)

        return structured_data

    async def research_specific_aspect(
        self,
        project_name: str,
        aspect: str  # 'tokenomics', 'technology', 'team', 'roadmap', 'competitors'
    ) -> dict:
        """
        Research specific aspect of a project.

        Args:
            project_name: Name of the crypto project
            aspect: Specific aspect to research

        Returns:
            dict: Detailed information about the specified aspect
        """
        query = f"{project_name} crypto project {aspect} details analysis"

        result = await self._tavily_research(query, deep_research=True)
        return await self._extract_aspect_data(result, aspect)

    async def find_competitors(
        self,
        project_name: str,
        project_category: str,
        features: List[str]
    ) -> List[dict]:
        """
        Find competitor projects using AI research.

        Args:
            project_name: Name of the project
            project_category: Category (DeFi, NFT, Layer 1, etc.)
            features: Key features to compare

        Returns:
            list: [
                {
                    'name': str,
                    'similarity': str,
                    'key_differences': list,
                    'advantages': list
                }
            ]
        """
        features_str = ", ".join(features)
        query = f"crypto projects similar to {project_name} in {project_category} with features: {features_str}"

        result = await self._tavily_research(query, deep_research=True)
        return await self._extract_competitors(result, project_name)

    async def get_market_data(
        self,
        project_name: str,
        contract_address: Optional[str] = None
    ) -> dict:
        """
        Get current market data for a project.

        Returns:
            dict: {
                'price': float,
                'market_cap': float,
                'volume_24h': float,
                'price_change_24h': float,
                'holders': int,
                'exchanges': list
            }
        """
        query = f"{project_name} crypto current price market cap volume"
        if contract_address:
            query += f" contract {contract_address}"

        result = await self._tavily_research(query, deep_research=False)
        return await self._extract_market_data(result)

    async def analyze_community(
        self,
        project_name: str
    ) -> dict:
        """
        Analyze community sentiment and activity.

        Returns:
            dict: {
                'twitter_followers': int,
                'discord_members': int,
                'telegram_members': int,
                'recent_news': list,
                'sentiment': str,
                'community_activity': str
            }
        """
        query = f"{project_name} crypto community twitter discord telegram activity sentiment"

        result = await self._tavily_research(query, deep_research=True)
        return await self._extract_community_data(result)

    # Private helper methods
    def _build_research_query(self, project_url: str, project_name: str = None) -> str:
        """Build comprehensive research query."""
        base = f"Comprehensive analysis of {project_url}"
        if project_name:
            base = f"Comprehensive analysis of {project_name} crypto project {project_url}"

        base += " including: features, tokenomics, technology, team, roadmap, use cases"
        return base

    async def _tavily_research(self, query: str, deep_research: bool = False) -> dict:
        """Execute Tavily research."""
        search_depth = "advanced" if deep_research else "basic"

        response = self.client.search(
            query=query,
            search_depth=search_depth,
            max_results=10,
            include_answer=True,
            include_raw_content=False
        )

        return response

    async def _perplexity_research(self, query: str) -> dict:
        """Execute Perplexity research (alternative)."""
        # Implement Perplexity API call
        # Note: Check Perplexity's actual API format
        pass

    async def _structure_research_results(self, raw_results: dict) -> dict:
        """
        Use LLM to structure raw research results.

        Takes unstructured research data and converts to structured format.
        """
        from common.llm_client import LLMClient

        llm = LLMClient()

        prompt = f"""
        Analyze this research data about a crypto project and extract structured information:

        Research Data:
        {raw_results.get('answer', '')}

        Sources:
        {raw_results.get('results', [])}

        Extract and return a JSON with:
        - summary: Brief project overview
        - description: Detailed description
        - key_features: List of main features
        - tokenomics: Token economics details
        - technology: Technical architecture
        - team: Team information
        - roadmap: Development roadmap
        - use_cases: Real-world applications
        - competitors: Similar projects
        """

        structured_data = await llm.generate(prompt, json_mode=True)
        return structured_data

    async def _extract_aspect_data(self, results: dict, aspect: str) -> dict:
        """Extract specific aspect from research results."""
        # Use LLM to extract and structure specific aspect
        pass

    async def _extract_competitors(self, results: dict, original_project: str) -> List[dict]:
        """Extract competitor information from research."""
        # Use LLM to identify and structure competitor data
        pass

    async def _extract_market_data(self, results: dict) -> dict:
        """Extract market data from research results."""
        # Use LLM to extract numerical market data
        pass

    async def _extract_community_data(self, results: dict) -> dict:
        """Extract community metrics from research."""
        # Use LLM to extract community information
        pass
```

**Implementation Notes:**
- Tavily AI is recommended for cost-effectiveness and quality
- Deep research mode provides more comprehensive results
- All research includes source citations for verification
- Use LLM (GPT-4o-mini) to structure raw research into standardized format
- Cache results to avoid redundant API calls
- Implement rate limiting per API service requirements
- Store raw research data along with structured data for auditing

**Cost Estimate:**
- Tavily: ~$0.005 per search, ~$0.05 per deep research
- Comprehensive project research: ~$0.10-0.20
- Much cheaper than maintaining web scrapers
- No infrastructure costs for proxies, browsers, etc.

#### 2. Document Parser (`document_parser.py`)

**Responsibilities:**
- Parse PDF whitepapers
- Extract text from DOCX files
- Process uploaded documents
- Extract key sections (tokenomics, roadmap, team)

**Key Functions:**

```python
def parse_whitepaper(file_path: str) -> dict:
    """
    Extract information from whitepaper PDF.

    Args:
        file_path: Path to PDF file

    Returns:
        dict: {
            'full_text': str,
            'tokenomics': dict,
            'roadmap': list,
            'team': list,
            'technical_details': str,
            'use_cases': list
        }
    """
    # Use PyPDF2 to extract text
    # Use LLM to structure information
    # Extract tables and figures
    pass

def extract_tokenomics(text: str) -> dict:
    """
    Use LLM to extract tokenomics details.

    Returns:
        dict: {
            'total_supply': str,
            'distribution': dict,
            'vesting': str,
            'utility': str
        }
    """
    pass
```

**Implementation Notes:**
- Handle different PDF formats
- Use OCR for image-based PDFs (if needed)
- Structure extraction using GPT-4o-mini
- Store raw and structured data

#### 3. Project Analyzer (`analyzer.py`)

**Responsibilities:**
- Analyze collected data
- Identify unique selling points
- Compare with competitors
- Generate project summary

**Key Functions:**

```python
async def analyze_project(project_data: dict) -> dict:
    """
    Analyze project and identify key features.

    Args:
        project_data: Combined data from scraper and parser

    Returns:
        dict: {
            'summary': str,
            'unique_features': list,
            'target_audience': str,
            'competitors': list,
            'strengths': list,
            'use_cases': list,
            'technical_innovation': str
        }
    """
    # Use LLM for analysis
    # Identify patterns
    # Generate insights
    pass

async def identify_competitors(project_category: str, features: list) -> list:
    """
    Find similar projects for comparison.

    Returns:
        list: [{'name': str, 'similarity_score': float, 'differences': list}]
    """
    pass
```

#### 4. Research API (`api.py`)

**FastAPI Endpoints:**

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class ProjectResearchRequest(BaseModel):
    url: HttpUrl
    contract_address: str = None
    include_social: bool = True

class DocumentUploadRequest(BaseModel):
    project_id: str
    document_type: str  # 'whitepaper', 'documentation', 'other'

@app.post("/research/start")
async def start_research(request: ProjectResearchRequest, background_tasks: BackgroundTasks):
    """
    Start research on a new project.

    Returns:
        {
            'project_id': str,
            'status': 'processing',
            'estimated_time': int (seconds)
        }
    """
    pass

@app.get("/research/status/{project_id}")
async def get_research_status(project_id: str):
    """
    Check research progress.

    Returns:
        {
            'project_id': str,
            'status': 'completed' | 'processing' | 'failed',
            'progress': int (0-100),
            'data': dict (if completed)
        }
    """
    pass

@app.post("/research/upload-document/{project_id}")
async def upload_document(project_id: str, file: UploadFile):
    """
    Upload additional documents for a project.

    Process the document and update project data.
    """
    pass

@app.get("/research/project/{project_id}")
async def get_project_data(project_id: str):
    """
    Retrieve complete project research data.
    """
    pass
```

---

## Text Generation Service

### Purpose
Generate various types of text content using LLMs.

### Components

#### 1. LLM Client (`llm_client.py`)

**Responsibilities:**
- Manage LLM API connections
- Handle different providers (OpenAI, Anthropic, Groq)
- Implement retry logic
- Track token usage

**Key Functions:**

```python
from typing import Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMClient:
    """Unified LLM client supporting multiple providers."""

    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini"):
        """
        Initialize LLM client.

        Args:
            provider: 'openai', 'anthropic', or 'groq'
            model: Model name
        """
        self.provider = provider
        self.model = model
        self._initialize_client()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        json_mode: bool = False
    ) -> str:
        """
        Generate text using LLM.

        Args:
            prompt: User prompt
            system_prompt: System instructions
            max_tokens: Maximum response length
            temperature: Creativity (0-1)
            json_mode: Return structured JSON

        Returns:
            str: Generated text
        """
        pass

    async def generate_with_context(
        self,
        messages: List[dict],
        **kwargs
    ) -> str:
        """
        Generate with conversation context.

        Args:
            messages: List of {'role': 'user/assistant', 'content': str}
        """
        pass

    def count_tokens(self, text: str) -> int:
        """Count tokens in text for cost estimation."""
        pass
```

**Implementation Notes:**
- Use environment variables for API keys
- Implement exponential backoff for rate limits
- Log all API calls for debugging
- Track costs per project

#### 2. Prompt Manager (`prompt_manager.py`)

**Responsibilities:**
- Store and manage prompt templates
- Dynamic prompt generation
- Version control for prompts

**Key Templates:**

```python
class PromptManager:
    """Manage prompt templates for different content types."""

    # Twitter Post Templates
    TWITTER_ANNOUNCEMENT = """
    You are a crypto content creator. Create an engaging Twitter post about {project_name}.

    Project Information:
    {project_info}

    Requirements:
    - Maximum 280 characters
    - Include 2-3 relevant hashtags
    - Engaging and professional tone
    - Highlight the key feature: {key_feature}
    - Include a call-to-action

    Generate the tweet:
    """

    TWITTER_THREAD = """
    Create a Twitter thread (5-7 tweets) explaining {topic} for {project_name}.

    Project Context:
    {project_context}

    Thread Structure:
    1. Hook - Grab attention
    2-3. Explanation - Break down the concept
    4-5. Benefits - Why it matters
    6. Call-to-action

    Each tweet must be under 280 characters.
    Number each tweet (1/7, 2/7, etc.)
    """

    # Project Description Templates
    PROJECT_SUMMARY = """
    Create a comprehensive project summary for {project_name}.

    Data Available:
    {research_data}

    Generate:
    1. One-line pitch (10-15 words)
    2. Short description (50 words)
    3. Detailed description (200 words)
    4. Key features (5 bullet points)
    5. Target audience

    Tone: Professional, clear, exciting but not hyperbolic
    """

    # Feature Explanation Templates
    FEATURE_EXPLAINER = """
    Explain the feature "{feature_name}" for {project_name} in simple terms.

    Technical Details:
    {technical_details}

    Create:
    1. Simple explanation (for beginners)
    2. Technical explanation (for developers)
    3. Real-world use case example
    4. Benefits compared to competitors

    Avoid jargon, use analogies where helpful.
    """

    # Comparison Templates
    COMPETITOR_COMPARISON = """
    Create a fair comparison between {project_name} and {competitor_name}.

    {project_name} Features:
    {our_features}

    {competitor_name} Features:
    {competitor_features}

    Generate:
    1. Side-by-side feature comparison table
    2. Unique advantages of {project_name}
    3. Areas where {competitor_name} excels
    4. Best use cases for each

    Be objective and fair.
    """

    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render a template with variables.

        Args:
            template_name: Name of the template
            **kwargs: Template variables

        Returns:
            str: Rendered prompt
        """
        pass
```

#### 3. Content Generators (`generators.py`)

**Responsibilities:**
- Generate specific content types
- Apply templates
- Format output

**Key Functions:**

```python
class ContentGenerator:
    """Generate various types of content."""

    def __init__(self, llm_client: LLMClient, prompt_manager: PromptManager):
        self.llm = llm_client
        self.prompts = prompt_manager

    async def generate_twitter_post(
        self,
        project_id: str,
        content_type: str = "announcement",
        key_point: str = None
    ) -> dict:
        """
        Generate Twitter post.

        Args:
            project_id: Project identifier
            content_type: 'announcement', 'feature', 'update', 'education'
            key_point: Specific point to highlight

        Returns:
            dict: {
                'text': str,
                'hashtags': list,
                'character_count': int,
                'suggested_image': str (description)
            }
        """
        pass

    async def generate_twitter_thread(
        self,
        project_id: str,
        topic: str,
        num_tweets: int = 7
    ) -> list:
        """
        Generate Twitter thread.

        Returns:
            list: [{'tweet_number': int, 'text': str, 'character_count': int}]
        """
        pass

    async def generate_project_description(
        self,
        project_id: str,
        length: str = "medium"  # 'short', 'medium', 'long'
    ) -> dict:
        """
        Generate project description.

        Returns:
            dict: {
                'one_liner': str,
                'short': str,
                'medium': str,
                'long': str,
                'key_features': list
            }
        """
        pass

    async def generate_feature_explanation(
        self,
        project_id: str,
        feature_name: str,
        audience: str = "general"  # 'general', 'technical', 'investor'
    ) -> dict:
        """
        Generate feature explanation.

        Returns:
            dict: {
                'simple_explanation': str,
                'technical_explanation': str,
                'use_case': str,
                'benefits': list
            }
        """
        pass

    async def generate_comparison(
        self,
        project_id: str,
        competitor_name: str
    ) -> dict:
        """
        Generate competitor comparison.
        """
        pass

    async def generate_blog_post(
        self,
        project_id: str,
        topic: str,
        word_count: int = 1000
    ) -> dict:
        """
        Generate long-form blog content.

        Returns:
            dict: {
                'title': str,
                'meta_description': str,
                'content': str (markdown),
                'outline': list,
                'seo_keywords': list
            }
        """
        pass
```

#### 4. Text Generation API (`api.py`)

**FastAPI Endpoints:**

```python
@app.post("/text/twitter/post")
async def generate_twitter_post(request: TwitterPostRequest):
    """
    Generate a single Twitter post.

    Request:
        {
            'project_id': str,
            'type': 'announcement' | 'feature' | 'update',
            'key_point': str (optional)
        }

    Returns:
        {
            'text': str,
            'hashtags': list,
            'metadata': dict
        }
    """
    pass

@app.post("/text/twitter/thread")
async def generate_twitter_thread(request: TwitterThreadRequest):
    """Generate Twitter thread."""
    pass

@app.post("/text/description")
async def generate_description(request: DescriptionRequest):
    """Generate project description."""
    pass

@app.post("/text/feature-explanation")
async def generate_feature_explanation(request: FeatureRequest):
    """Generate feature explanation."""
    pass

@app.post("/text/blog-post")
async def generate_blog_post(request: BlogPostRequest):
    """Generate blog post."""
    pass
```

---

## Image Generation Service

### Purpose
Generate branded images using Nano Banana API with consistent style and mascot.

### Components

#### 1. Nano Banana Client (`nano_banana.py`)

**Responsibilities:**
- Interface with Nano Banana API
- Handle image generation requests
- Download and store images
- Manage API rate limits

**Key Functions:**

```python
class NanoBananaClient:
    """Client for Nano Banana image generation API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nanobanana.ai/v1"  # Adjust to actual URL

    @retry(stop=stop_after_attempt(3))
    async def generate_image(
        self,
        prompt: str,
        style: str = None,
        aspect_ratio: str = "1:1",
        model: str = "default"
    ) -> dict:
        """
        Generate image using Nano Banana.

        Args:
            prompt: Image generation prompt
            style: Style preset
            aspect_ratio: '1:1', '16:9', '9:16', '4:5'
            model: Model version

        Returns:
            dict: {
                'image_url': str,
                'image_id': str,
                'generation_time': float,
                'cost': float
            }
        """
        pass

    async def download_image(self, image_url: str, save_path: str) -> str:
        """
        Download generated image.

        Returns:
            str: Local file path
        """
        pass

    async def get_generation_status(self, generation_id: str) -> dict:
        """
        Check status of async generation.

        Returns:
            dict: {
                'status': 'pending' | 'completed' | 'failed',
                'image_url': str (if completed)
            }
        """
        pass
```

**Implementation Notes:**
- Check Nano Banana's actual API documentation
- Handle async generation if API is not instant
- Store API responses for debugging
- Implement webhook handling for async results

#### 2. Style Manager (`style_manager.py`)

**Responsibilities:**
- Maintain brand consistency
- Manage mascot appearances
- Store style presets
- Generate style-consistent prompts

**Key Functions:**

```python
class StyleManager:
    """Manage brand style and mascot consistency."""

    def __init__(self, brand_config_path: str):
        """
        Load brand configuration.

        Config includes:
        - Mascot description
        - Color palette
        - Visual style
        - Logo elements
        """
        self.brand_config = self._load_config(brand_config_path)

    def apply_brand_style(self, base_prompt: str, include_mascot: bool = True) -> str:
        """
        Enhance prompt with brand elements.

        Args:
            base_prompt: Basic image description
            include_mascot: Whether to include mascot

        Returns:
            str: Enhanced prompt with brand style

        Example:
            Input: "rocket launching into space"
            Output: "rocket launching into space, with [mascot name] cheering,
                    vibrant colors [brand colors], modern digital art style,
                    [style keywords]"
        """
        pass

    def get_mascot_prompt(self, emotion: str = "happy", action: str = None) -> str:
        """
        Generate consistent mascot description.

        Args:
            emotion: 'happy', 'excited', 'thinking', 'surprised'
            action: Specific action mascot is doing

        Returns:
            str: Detailed mascot description for consistency
        """
        pass

    def get_style_preset(self, content_type: str) -> dict:
        """
        Get style configuration for content type.

        Args:
            content_type: 'social_media', 'infographic', 'header', 'announcement'

        Returns:
            dict: {
                'aspect_ratio': str,
                'style_keywords': list,
                'color_scheme': str,
                'composition': str
            }
        """
        pass

    def validate_brand_consistency(self, generated_image_path: str) -> dict:
        """
        Analyze if image matches brand (optional advanced feature).

        Returns:
            dict: {
                'has_mascot': bool,
                'color_match': float (0-1),
                'style_match': float (0-1),
                'approved': bool
            }
        """
        pass
```

#### 3. Image Templates (`templates.py`)

**Responsibilities:**
- Predefined image templates
- Template-based prompt generation
- Layout specifications

**Key Functions:**

```python
class ImageTemplateManager:
    """Manage image generation templates."""

    TEMPLATES = {
        'twitter_announcement': {
            'aspect_ratio': '16:9',
            'structure': 'centered text with mascot, clean background',
            'prompt_template': '{mascot} holding a sign that says "{text}", {brand_style}, professional social media post'
        },
        'feature_highlight': {
            'aspect_ratio': '1:1',
            'structure': 'feature icon, mascot, descriptive text',
            'prompt_template': '{mascot} showcasing {feature_name}, {feature_visual}, {brand_style}, informative and clean'
        },
        'infographic': {
            'aspect_ratio': '4:5',
            'structure': 'data visualization with mascot guide',
            'prompt_template': 'infographic about {topic}, {mascot} as guide, {data_points}, {brand_style}, modern and clear'
        },
        'comparison': {
            'aspect_ratio': '16:9',
            'structure': 'side-by-side comparison',
            'prompt_template': 'comparison chart showing {project_name} vs {competitor}, {mascot} pointing out advantages, {brand_style}'
        },
        'announcement': {
            'aspect_ratio': '16:9',
            'structure': 'bold announcement with mascot',
            'prompt_template': '{mascot} excited about {announcement}, dramatic and eye-catching, {brand_style}, celebration'
        }
    }

    def generate_from_template(
        self,
        template_name: str,
        **variables
    ) -> dict:
        """
        Generate image prompt from template.

        Args:
            template_name: Name of the template
            **variables: Template variables

        Returns:
            dict: {
                'prompt': str,
                'aspect_ratio': str,
                'style_config': dict
            }
        """
        pass

    def create_custom_template(
        self,
        name: str,
        structure: str,
        prompt_template: str,
        aspect_ratio: str = "1:1"
    ) -> None:
        """
        Add custom template to library.
        """
        pass
```

#### 4. Image Generation API (`api.py`)

**FastAPI Endpoints:**

```python
@app.post("/image/generate")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate branded image.

    Request:
        {
            'project_id': str,
            'template': str,
            'variables': dict,
            'custom_prompt': str (optional)
        }

    Returns:
        {
            'image_id': str,
            'image_url': str,
            'local_path': str,
            'prompt_used': str
        }
    """
    pass

@app.post("/image/from-template")
async def generate_from_template(request: TemplateImageRequest):
    """Generate image using predefined template."""
    pass

@app.get("/image/styles")
async def get_available_styles():
    """List available style presets."""
    pass

@app.post("/image/batch")
async def generate_batch_images(request: BatchImageRequest):
    """Generate multiple images in one request."""
    pass
```

---

## Video Generation Service

### Purpose
Generate AI videos using VEO3.1 API with project-specific scripts.

### Components

#### 1. VEO3.1 Client (`veo_client.py`)

**Responsibilities:**
- Interface with VEO3.1 API
- Handle video generation requests
- Monitor generation progress
- Download completed videos

**Key Functions:**

```python
class VEOClient:
    """Client for VEO3.1 video generation API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.veo.ai/v3.1"  # Adjust to actual URL

    @retry(stop=stop_after_attempt(3))
    async def generate_video(
        self,
        prompt: str,
        duration: int = 5,  # seconds
        aspect_ratio: str = "16:9",
        style: str = None,
        audio: bool = False
    ) -> dict:
        """
        Generate video using VEO3.1.

        Args:
            prompt: Video generation prompt (detailed scene description)
            duration: Video length in seconds
            aspect_ratio: '16:9', '9:16', '1:1'
            style: Style preset
            audio: Include AI-generated audio

        Returns:
            dict: {
                'generation_id': str,
                'status': 'processing',
                'estimated_completion': int (seconds)
            }
        """
        pass

    async def get_generation_status(self, generation_id: str) -> dict:
        """
        Check video generation status.

        Returns:
            dict: {
                'status': 'processing' | 'completed' | 'failed',
                'progress': int (0-100),
                'video_url': str (if completed),
                'error': str (if failed)
            }
        """
        pass

    async def download_video(self, video_url: str, save_path: str) -> str:
        """
        Download generated video.

        Returns:
            str: Local file path
        """
        pass

    async def cancel_generation(self, generation_id: str) -> bool:
        """Cancel ongoing video generation."""
        pass
```

**Implementation Notes:**
- Check VEO3.1 actual API documentation
- Video generation is likely async (takes time)
- Implement polling or webhook for completion
- Handle large file downloads efficiently

#### 2. Script Generator (`script_generator.py`)

**Responsibilities:**
- Generate video scripts from project data
- Create detailed scene descriptions
- Plan video structure

**Key Functions:**

```python
class VideoScriptGenerator:
    """Generate video scripts and prompts."""

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    async def generate_intro_video_script(
        self,
        project_id: str,
        duration: int = 30
    ) -> dict:
        """
        Generate project introduction video script.

        Args:
            project_id: Project identifier
            duration: Target video length in seconds

        Returns:
            dict: {
                'script': str,
                'scenes': [
                    {
                        'scene_number': int,
                        'duration': int (seconds),
                        'description': str (detailed visual description),
                        'narration': str (voice-over text),
                        'visual_prompt': str (for VEO3.1)
                    }
                ],
                'total_duration': int
            }
        """
        pass

    async def generate_feature_explainer_script(
        self,
        project_id: str,
        feature_name: str,
        duration: int = 45
    ) -> dict:
        """
        Generate feature explanation video script.
        """
        pass

    async def generate_tutorial_script(
        self,
        project_id: str,
        tutorial_topic: str,
        duration: int = 60
    ) -> dict:
        """
        Generate tutorial video script.
        """
        pass

    def create_scene_prompt(self, scene_description: str, brand_style: dict) -> str:
        """
        Convert scene description to VEO3.1 prompt.

        Args:
            scene_description: High-level scene description
            brand_style: Brand styling configuration

        Returns:
            str: Detailed prompt for video generation

        Example:
            Input: "Mascot explaining tokenomics"
            Output: "[Mascot name] standing in front of animated chart showing
                    token distribution, pointing at different segments, bright
                    professional background, smooth camera movement, [brand colors]"
        """
        pass
```

#### 3. Video Templates (`templates.py`)

**Responsibilities:**
- Predefined video structures
- Template-based script generation

**Key Templates:**

```python
class VideoTemplateManager:
    """Manage video generation templates."""

    TEMPLATES = {
        'project_intro': {
            'duration': 30,
            'structure': [
                {'type': 'hook', 'duration': 5, 'goal': 'grab attention'},
                {'type': 'problem', 'duration': 8, 'goal': 'explain problem'},
                {'type': 'solution', 'duration': 12, 'goal': 'introduce project'},
                {'type': 'cta', 'duration': 5, 'goal': 'call to action'}
            ]
        },
        'feature_showcase': {
            'duration': 45,
            'structure': [
                {'type': 'intro', 'duration': 5},
                {'type': 'feature_demo', 'duration': 25},
                {'type': 'benefits', 'duration': 10},
                {'type': 'cta', 'duration': 5}
            ]
        },
        'tutorial': {
            'duration': 60,
            'structure': [
                {'type': 'intro', 'duration': 5},
                {'type': 'overview', 'duration': 10},
                {'type': 'step_by_step', 'duration': 35},
                {'type': 'recap', 'duration': 10}
            ]
        }
    }

    def generate_template_script(
        self,
        template_name: str,
        project_data: dict,
        **custom_params
    ) -> dict:
        """
        Generate script based on template.
        """
        pass
```

#### 4. Video Generation API (`api.py`)

**FastAPI Endpoints:**

```python
@app.post("/video/generate-script")
async def generate_video_script(request: ScriptGenerationRequest):
    """
    Generate video script.

    Request:
        {
            'project_id': str,
            'video_type': 'intro' | 'feature' | 'tutorial',
            'duration': int,
            'custom_requirements': str (optional)
        }

    Returns:
        {
            'script_id': str,
            'script': dict (with scenes),
            'estimated_production_time': int
        }
    """
    pass

@app.post("/video/generate")
async def generate_video(request: VideoGenerationRequest):
    """
    Generate video from script.

    Request:
        {
            'script_id': str,
            'scene_numbers': list (optional, generate specific scenes),
            'style': str (optional)
        }

    Returns:
        {
            'generation_id': str,
            'status': 'processing',
            'estimated_completion_time': int (minutes)
        }
    """
    pass

@app.get("/video/status/{generation_id}")
async def get_video_status(generation_id: str):
    """Check video generation status."""
    pass

@app.get("/video/download/{generation_id}")
async def download_video(generation_id: str):
    """Download completed video."""
    pass
```

---

## Common Utilities

### Purpose
Shared functionality across all services.

### Components

#### 1. Configuration Management (`config.py`)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None
    NANO_BANANA_API_KEY: str
    VEO_API_KEY: str

    # AI Research Services
    TAVILY_API_KEY: str
    PERPLEXITY_API_KEY: Optional[str] = None
    EXA_API_KEY: Optional[str] = None

    # Research Configuration
    DEFAULT_RESEARCH_SERVICE: str = "tavily"
    DEEP_RESEARCH_MODE: bool = True

    # LLM Configuration
    DEFAULT_LLM_PROVIDER: str = "openai"
    DEFAULT_LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000

    # Database
    DATABASE_URL: str = "sqlite:///./data/crypto_content.db"

    # File Storage
    DATA_DIR: str = "./data"
    PROJECTS_DIR: str = "./data/projects"
    CONTENT_DIR: str = "./data/content"

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

#### 2. Database Operations (`database.py`)

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Project(Base):
    """Project information table."""
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)
    contract_address = Column(String)

    # Research data
    research_data = Column(JSON)
    research_status = Column(String)  # 'pending', 'processing', 'completed', 'failed'
    research_completed_at = Column(DateTime)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GeneratedContent(Base):
    """Generated content tracking table."""
    __tablename__ = "generated_content"

    id = Column(String, primary_key=True)
    project_id = Column(String, nullable=False)
    content_type = Column(String)  # 'text', 'image', 'video'
    content_subtype = Column(String)  # 'twitter_post', 'description', etc.

    # Content data
    content_data = Column(JSON)  # Actual content or reference
    file_path = Column(String)  # For images/videos

    # Generation metadata
    prompt_used = Column(Text)
    model_used = Column(String)
    generation_cost = Column(String)  # Track costs

    # Status
    status = Column(String)  # 'pending', 'processing', 'completed', 'failed'
    error_message = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

# Database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
```

#### 3. Data Models (`models.py`)

```python
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict
from datetime import datetime

# Request Models
class ProjectResearchRequest(BaseModel):
    url: HttpUrl
    contract_address: Optional[str] = None
    include_social: bool = True

class TwitterPostRequest(BaseModel):
    project_id: str
    type: str = Field(..., pattern="^(announcement|feature|update|education)$")
    key_point: Optional[str] = None

class ImageGenerationRequest(BaseModel):
    project_id: str
    template: str
    variables: Dict[str, str]
    custom_prompt: Optional[str] = None

# Response Models
class ProjectResearchResponse(BaseModel):
    project_id: str
    status: str
    progress: int = Field(..., ge=0, le=100)
    data: Optional[Dict] = None

class TwitterPostResponse(BaseModel):
    text: str
    hashtags: List[str]
    character_count: int
    suggested_image: Optional[str] = None

class GenerationStatusResponse(BaseModel):
    generation_id: str
    status: str
    progress: int
    result_url: Optional[str] = None
    error: Optional[str] = None
```

#### 4. Logging (`logger.py`)

```python
import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """
    Set up logger with console and file handlers.

    Args:
        name: Logger name
        log_file: Optional file path for logs
        level: Logging level

    Returns:
        logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger
```

#### 5. Utility Functions (`utils.py`)

```python
import hashlib
import uuid
from pathlib import Path
from typing import Optional

def generate_project_id(url: str) -> str:
    """Generate unique project ID from URL."""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def generate_content_id() -> str:
    """Generate unique content ID."""
    return str(uuid.uuid4())

def ensure_directory(path: str) -> Path:
    """Ensure directory exists, create if not."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()

def estimate_token_count(text: str) -> int:
    """Rough estimate of token count (1 token ≈ 4 characters)."""
    return len(text) // 4

def calculate_cost(tokens: int, model: str) -> float:
    """
    Calculate LLM cost based on tokens and model.

    Prices per 1M tokens:
    - gpt-4o-mini: $0.15 input, $0.60 output
    - claude-haiku: $0.25 input, $1.25 output
    """
    pricing = {
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        'claude-haiku': {'input': 0.25, 'output': 1.25}
    }

    if model in pricing:
        # Assume 70% input, 30% output ratio
        cost = (tokens * 0.7 * pricing[model]['input'] +
                tokens * 0.3 * pricing[model]['output']) / 1_000_000
        return round(cost, 6)

    return 0.0
```

---

## Main Application

### Main FastAPI App (`main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from common.config import settings
from common.database import init_db
from common.logger import setup_logger

# Import service routers
from research.api import app as research_app
from text_gen.api import app as text_app
from image_gen.api import app as image_app
from video_gen.api import app as video_app

# Setup logger
logger = setup_logger(__name__, "logs/main.log")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting Crypto Content Automation API")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down API")

# Create main app
app = FastAPI(
    title="Crypto Content Automation API",
    description="AI-powered content generation for crypto projects",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount service apps
app.mount("/api/research", research_app)
app.mount("/api/text", text_app)
app.mount("/api/image", image_app)
app.mount("/api/video", video_app)

@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Crypto Content Automation API",
        "version": "1.0.0",
        "services": {
            "research": "/api/research/docs",
            "text": "/api/text/docs",
            "image": "/api/image/docs",
            "video": "/api/video/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True  # Disable in production
    )
```

---

## Environment Setup

### .env.example

```env
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
NANO_BANANA_API_KEY=your_nano_banana_key_here
VEO_API_KEY=your_veo_key_here

# AI Research Services
TAVILY_API_KEY=your_tavily_key_here
# PERPLEXITY_API_KEY=your_perplexity_key_here  # Alternative
# EXA_API_KEY=your_exa_key_here  # Alternative

# Research Configuration
DEFAULT_RESEARCH_SERVICE=tavily
DEEP_RESEARCH_MODE=true

# LLM Configuration
DEFAULT_LLM_PROVIDER=openai
DEFAULT_LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Database
DATABASE_URL=sqlite:///./data/crypto_content.db

# File Storage
DATA_DIR=./data
PROJECTS_DIR=./data/projects
CONTENT_DIR=./data/content

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_llm_client.py
import pytest
from text_gen.llm_client import LLMClient

@pytest.mark.asyncio
async def test_generate_simple_text():
    client = LLMClient(provider="openai", model="gpt-4o-mini")
    result = await client.generate("Say hello")
    assert isinstance(result, str)
    assert len(result) > 0

# tests/test_ai_researcher.py
@pytest.mark.asyncio
async def test_research_project():
    from research.ai_researcher import AIResearcher
    researcher = AIResearcher(api_key="test_key", service="tavily")
    result = await researcher.research_project("https://example.com", "Example Project")
    assert "summary" in result
    assert "key_features" in result
    assert "sources" in result
```

### Integration Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_start_research():
    response = client.post(
        "/api/research/start",
        json={"url": "https://example.com"}
    )
    assert response.status_code == 200
    assert "project_id" in response.json()
```

---

## Development Workflow

### 1. Initial Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -c "from common.database import init_db; init_db()"
```

### 2. Development Server

```bash
# Run development server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_llm_client.py

# Run with coverage
pytest --cov=python-services tests/
```

---

## Implementation Priority

### Phase 1: Core Infrastructure (Week 1)
1. Set up project structure
2. Implement configuration management
3. Set up database models
4. Create logging utilities
5. Basic FastAPI app with health check

### Phase 2: Research Service (Week 1-2)
1. Web scraper for basic site data
2. Document parser for PDFs
3. Basic project analyzer
4. Research API endpoints
5. Database integration

### Phase 3: Text Generation (Week 2-3)
1. LLM client implementation
2. Prompt template system
3. Twitter post generator
4. Project description generator
5. Text API endpoints

### Phase 4: Image Generation (Week 3-4)
1. Nano Banana API client
2. Style management system
3. Image templates
4. Image API endpoints

### Phase 5: Video Generation (Week 4-5)
1. VEO3.1 API client
2. Script generator
3. Video templates
4. Video API endpoints

### Phase 6: Integration & Testing (Week 5-6)
1. End-to-end testing
2. Error handling improvements
3. Performance optimization
4. Documentation

---

## Best Practices

### Code Quality
- Use type hints throughout
- Follow PEP 8 style guide
- Write docstrings for all functions
- Implement proper error handling
- Use async/await for I/O operations

### Security
- Never commit API keys
- Validate all inputs
- Sanitize file paths
- Use environment variables
- Implement rate limiting

### Performance
- Cache frequently accessed data
- Use batch processing where possible
- Implement connection pooling
- Monitor API usage and costs
- Optimize database queries

### Logging
- Log all API calls
- Track errors with context
- Monitor generation costs
- Log performance metrics
- Use structured logging

---

## Next Steps

1. Review this implementation guide
2. Set up development environment
3. Start with Phase 1 (Core Infrastructure)
4. Implement services incrementally
5. Test each component thoroughly
6. Integrate with n8n workflows

This guide provides a complete roadmap for the Python implementation. Each section can be developed incrementally and tested independently before integration.
