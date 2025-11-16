# Crypto Content Automation System

An AI-powered content automation system for crypto projects, featuring automated research, text generation, image creation, and video production.

## Overview

This project combines Python microservices with n8n workflow orchestration to create a comprehensive content generation system for cryptocurrency projects. It uses AI services to research projects and generate engaging content across multiple formats.

## Features

- **AI-Powered Research**: Automated project analysis using Tavily AI and web scraping
- **Text Generation**: LLM-based content creation (Twitter posts, descriptions, blog posts)
- **Image Generation**: Branded images with consistent mascot using Nano Banana API
- **Video Generation**: AI-generated videos using VEO3.1 API
- **Workflow Orchestration**: n8n integration for scheduling and automation

## Project Structure

```
robocont/
├── python-services/         # Python microservices
│   ├── research/           # Project research & analysis
│   ├── text-gen/           # LLM text generation
│   ├── image-gen/          # Image generation
│   ├── video-gen/          # Video generation
│   ├── common/             # Shared utilities
│   ├── main.py            # FastAPI application
│   └── requirements.txt   # Python dependencies
├── workflows/              # n8n workflow definitions
├── data/                   # Data storage
│   ├── projects/          # Project research data
│   ├── content/           # Generated content
│   └── templates/         # Brand templates
├── config/                 # Configuration files
├── docs/                   # Documentation
├── logs/                   # Application logs
├── PROJECT_PLAN.md        # Detailed project plan
└── PYTHON_IMPLEMENTATION_GUIDE.md  # Implementation guide
```

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- API Keys:
  - OpenAI API key (for LLM)
  - Tavily API key (for research)
  - Nano Banana API key (for images)
  - VEO API key (for videos)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd robocont
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
cd python-services
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
NANO_BANANA_API_KEY=your_nano_banana_key_here
VEO_API_KEY=your_veo_key_here
```

### 4. Initialize Database

```bash
python -c "from common.database import init_db; init_db()"
```

## Running the Application

### Development Server

```bash
cd python-services
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API Root: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Services

### Research Service
- `POST /api/research/start` - Start project research
- `GET /api/research/status/{project_id}` - Check research status
- `GET /api/research/project/{project_id}` - Get project data

### Text Generation Service
- `POST /api/text/twitter/post` - Generate Twitter post
- `POST /api/text/twitter/thread` - Generate Twitter thread
- `POST /api/text/description` - Generate project description

### Image Generation Service
- `POST /api/image/generate` - Generate branded image
- `POST /api/image/from-template` - Generate from template
- `GET /api/image/styles` - List available styles

### Video Generation Service
- `POST /api/video/generate-script` - Generate video script
- `POST /api/video/generate` - Generate video
- `GET /api/video/status/{generation_id}` - Check generation status

## Development Status

### ✅ Phase 1: Core Infrastructure (Completed)
- [x] Project structure
- [x] Configuration management
- [x] Database models
- [x] Logging utilities
- [x] FastAPI application skeleton

### 🚧 Phase 2: Research Service (In Development)
- [x] Service skeleton
- [ ] AI researcher implementation
- [ ] Document parser
- [ ] Project analyzer
- [ ] API endpoints

### 📋 Phase 3: Text Generation (Planned)
- [x] Service skeleton
- [ ] LLM client integration
- [ ] Prompt templates
- [ ] Content generators
- [ ] API endpoints

### 📋 Phase 4: Image Generation (Planned)
- [x] Service skeleton
- [ ] Nano Banana integration
- [ ] Style management
- [ ] Template system
- [ ] API endpoints

### 📋 Phase 5: Video Generation (Planned)
- [x] Service skeleton
- [ ] VEO3.1 integration
- [ ] Script generator
- [ ] Template system
- [ ] API endpoints

### 📋 Phase 6: n8n Integration (Planned)
- [ ] Workflow definitions
- [ ] Scheduling
- [ ] Automation
- [ ] Error handling

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_llm_client.py

# Run with coverage
pytest --cov=python-services tests/
```

## Architecture

### Hybrid Approach
- **Python Services**: Handle AI/ML operations, complex data processing
- **n8n Workflows**: Orchestrate services, schedule tasks, handle webhooks

### Technology Stack
- **FastAPI**: Async web framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **Tavily AI**: Research service
- **OpenAI**: Text generation
- **Nano Banana**: Image generation
- **VEO3.1**: Video generation

## Documentation

- [PROJECT_PLAN.md](./PROJECT_PLAN.md) - Comprehensive project plan with development batches
- [PYTHON_IMPLEMENTATION_GUIDE.md](./PYTHON_IMPLEMENTATION_GUIDE.md) - Detailed implementation guide

## Contributing

This is a private project. For questions or issues, please contact the project maintainer.

## License

Private project - All rights reserved.

## Cost Estimates

Expected monthly costs (moderate usage):
- LLM (GPT-4o-mini): ~$10-30/month
- Tavily AI Research: ~$5-15/month
- Nano Banana API: TBD (check pricing)
- VEO3.1 API: TBD (check pricing)
- n8n hosting (if cloud): $20-50/month or free (self-hosted)

**Total**: ~$35-95/month (excluding image/video API costs)

## Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review the implementation guides
3. Check API documentation at `/docs` endpoint

## Next Steps

1. ✅ Review instruction files
2. ✅ Set up project structure
3. ✅ Create service skeletons
4. 🚧 Implement research service
5. 📋 Implement text generation
6. 📋 Implement image generation
7. 📋 Implement video generation
8. 📋 Create n8n workflows
9. 📋 Test end-to-end functionality
10. 📋 Deploy and monitor
