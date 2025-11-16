# Python Services - Crypto Content Automation

This directory contains all Python microservices for the crypto content automation system.

## Services

### 1. Research Service (`research/`)
AI-powered research and analysis of crypto projects.

**Components:**
- `ai_researcher.py` - Tavily AI integration for project research
- `document_parser.py` - PDF and document parsing
- `analyzer.py` - Project analysis and insights
- `api.py` - FastAPI endpoints

**Endpoints:**
- `POST /api/research/start` - Start project research
- `GET /api/research/status/{project_id}` - Check status
- `GET /api/research/project/{project_id}` - Get research data

### 2. Text Generation Service (`text-gen/`)
LLM-based text content generation.

**Components:**
- `llm_client.py` - Unified LLM client (OpenAI, Anthropic, Hermes)
- `prompt_manager.py` - Prompt template management
- `generators.py` - Content generation functions
- `api.py` - FastAPI endpoints

**Endpoints:**
- `POST /api/text/twitter/post` - Generate Twitter post
- `POST /api/text/twitter/thread` - Generate Twitter thread
- `POST /api/text/description` - Generate project description

### 3. Image Generation Service (`image-gen/`)
Branded image creation using Nano Banana API.

**Components:**
- `nano_banana.py` - Nano Banana API client
- `style_manager.py` - Brand style and mascot consistency
- `templates.py` - Image generation templates
- `api.py` - FastAPI endpoints

**Endpoints:**
- `POST /api/image/generate` - Generate branded image
- `POST /api/image/from-template` - Use predefined template
- `GET /api/image/styles` - List available styles

### 4. Video Generation Service (`video-gen/`)
AI-generated videos using VEO3.1 API.

**Components:**
- `veo_client.py` - VEO3.1 API client
- `script_generator.py` - Video script creation
- `templates.py` - Video templates
- `api.py` - FastAPI endpoints

**Endpoints:**
- `POST /api/video/generate-script` - Generate video script
- `POST /api/video/generate` - Generate video from script
- `GET /api/video/status/{generation_id}` - Check generation status

### 5. Common Utilities (`common/`)
Shared functionality across all services.

**Components:**
- `config.py` - Configuration management
- `database.py` - SQLAlchemy models and database operations
- `models.py` - Pydantic request/response models
- `logger.py` - Logging configuration
- `utils.py` - Helper functions

## Quick Start

### 1. Install Dependencies

```bash
cd python-services
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Initialize Database

```bash
python -c "from common.database import init_db; init_db()"
```

### 4. Run Development Server

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Environment Variables

Required:
- `OPENAI_API_KEY` - OpenAI API key for text generation
- `TAVILY_API_KEY` - Tavily AI for research
- `NANO_BANANA_API_KEY` - Nano Banana for images
- `VEO_API_KEY` - VEO3.1 for videos

Optional:
- `ANTHROPIC_API_KEY` - Alternative LLM provider (Claude models)
- `HERMES_API_KEY` - Alternative LLM provider (Hermes models from Nous Research)
- `HERMES_API_URL` - Hermes API base URL (default: https://inference-api.nousresearch.com)
- `DATABASE_URL` - Database connection string
- `API_PORT` - API server port (default: 8000)

See `.env.example` for complete list.

## Development

### Adding a New Endpoint

1. Define request/response models in `common/models.py`
2. Implement business logic in the service module
3. Add endpoint in service's `api.py`
4. Update tests

### Running Tests

```bash
pytest
pytest --cov=. tests/  # with coverage
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Use async/await for I/O operations

## Project Status

- ✅ Core infrastructure complete
- ✅ Service skeletons created
- 🚧 Implementation in progress
- 📋 Testing pending
- 📋 n8n integration pending

## Next Steps

1. Implement AI researcher with Tavily integration
2. Complete LLM client integration
3. Implement Nano Banana API client
4. Implement VEO3.1 API client
5. Add comprehensive testing
6. Create n8n workflows
