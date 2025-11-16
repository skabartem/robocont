# Crypto Content Automation System - Project Plan

## Project Overview

Automated system for creating AI-generated content for crypto projects, including:
- AI videos (VEO3.1 API)
- Images with mascot and brand style (Nano Banana)
- Text content and Twitter posts (Cost-effective LLM)
- Automated project research and analysis

## System Architecture

### Hybrid Approach: n8n + Python

**Why this combination:**
- **n8n**: Workflow orchestration, scheduling, webhook handling, simple integrations
- **Python**: AI/ML operations, web scraping, complex data processing, API integrations with AI services

### Project Structure

```
crypto-content-automation/
├── workflows/              # n8n workflow JSON files (version controlled)
├── python-services/        # Python microservices
│   ├── research/          # Project research & analysis
│   ├── text-gen/          # LLM text generation
│   ├── image-gen/         # Nano Banana integration
│   ├── video-gen/         # VEO3.1 integration
│   └── common/            # Shared utilities
├── data/                  # Local storage
│   ├── projects/          # Project research data
│   ├── content/           # Generated content
│   │   ├── images/
│   │   ├── videos/
│   │   └── text/
│   └── templates/         # Brand templates, prompts
├── config/                # Configuration files
└── docs/                  # Documentation
```

## Tech Stack

### Orchestration
- **n8n** (self-hosted or cloud)

### Python Services
- **FastAPI** - Lightweight API framework for Python services
- **LangChain or LlamaIndex** - For LLM orchestration
- **Beautiful Soup / Playwright** - Web scraping
- **httpx / requests** - API calls

### LLM for Text Generation (Cost-effective options)
- **Recommended**: OpenAI GPT-4o-mini (~$0.15/1M input tokens) - best quality/price
- **Alternative**: Anthropic Claude Haiku (~$0.25/1M tokens)
- **Alternative**: Groq (free tier, very fast)
- **Alternative**: Local Llama models (free but requires GPU)

### Image Generation
- **Nano Banana API**

### Video Generation
- **VEO3.1 API**

### Database (optional but recommended)
- **SQLite** - Simple, file-based, no server needed
- Stores: project metadata, generation history, content status

### Storage
- **Local file system** - For generated content and project data

## Development Batches

### Batch 1: Foundation (Week 1-2)
**Objectives:**
- Set up GitHub repository
- Initialize Python project structure
- Set up n8n (local or cloud)
- Create basic project research module
- Database schema design

**Deliverables:**
- Working repository with organized structure
- Basic Python environment with dependencies
- n8n installation and initial configuration
- SQLite database with initial schema

---

### Batch 2: Research & Analysis (Week 2-3)
**Objectives:**
- Web scraping for crypto projects
- Document processing for updates
- Extract key features, tokenomics, USPs
- Store structured project data

**Deliverables:**
- Web scraping modules for crypto data sources
- Document parser for manual uploads
- Data extraction pipeline
- Structured storage of project information

**Data Sources:**
- Project websites
- Whitepapers (PDF processing)
- CoinGecko/CoinMarketCap APIs
- Social media (Twitter, Discord, Telegram)
- Block explorers

---

### Batch 3: Text Generation (Week 3-4)
**Objectives:**
- LLM integration for text generation
- Prompt templates for different content types
- Twitter post generation
- Project description generation

**Deliverables:**
- LLM API integration
- Prompt template system
- Text generation service with API
- Multiple content type generators:
  - Twitter posts (threads and single posts)
  - Project descriptions
  - Feature highlights
  - Comparisons with competitors

---

### Batch 4: Image Generation (Week 4-5)
**Objectives:**
- Nano Banana API integration
- Mascot/brand consistency system
- Template management
- Automated image generation workflow

**Deliverables:**
- Nano Banana integration
- Image generation service with API
- Brand style management system
- Mascot consistency framework
- Image templates for different use cases:
  - Social media posts
  - Infographics
  - Feature highlights
  - Announcements

---

### Batch 5: Video Generation (Week 5-6)
**Objectives:**
- VEO3.1 API integration
- Script generation for videos
- Video style templates
- Rendering workflow

**Deliverables:**
- VEO3.1 API integration
- Video script generator
- Video generation service with API
- Video templates:
  - Project introductions
  - Feature explainers
  - Tutorial videos
  - Announcement videos

---

### Batch 6: Orchestration & Automation (Week 6-7)
**Objectives:**
- n8n workflows connecting all services
- Scheduling and triggers
- Content publishing pipelines
- Error handling and monitoring

**Deliverables:**
- Complete n8n workflows for:
  - New project onboarding
  - Scheduled content generation
  - Content review and approval
  - Multi-platform publishing
- Error handling and retry logic
- Monitoring and logging system
- Webhook triggers for manual interventions

---

### Batch 7: Polish & Documentation (Week 7-8)
**Objectives:**
- Testing and refinement
- Documentation
- Deployment guide
- Usage examples

**Deliverables:**
- Comprehensive documentation
- Setup and installation guide
- API documentation
- Usage tutorials and examples
- Troubleshooting guide
- Best practices document

## Input Sources

**Primary Input:**
- Initial automatic research of crypto projects
- Manual document uploads for project updates

**Research Process:**
1. Automatic discovery (optional future feature)
2. Manual project URL/contract address input
3. Automated web scraping and data collection
4. Document processing (whitepapers, documentation)
5. Periodic updates with new information

## System Workflow

```
1. Project Input (URL/Address/Documents)
   ↓
2. Research & Analysis (Python Service)
   ↓
3. Data Storage (SQLite + File System)
   ↓
4. Content Generation Trigger (n8n)
   ↓
5. Parallel Content Creation:
   - Text Generation (Python + LLM)
   - Image Generation (Python + Nano Banana)
   - Video Generation (Python + VEO3.1)
   ↓
6. Content Review & Approval (Optional Manual Step)
   ↓
7. Publishing (n8n Workflow)
```

## Key Features

### Project Research
- Automated web scraping
- Whitepaper analysis
- Social media monitoring
- Competitor analysis
- Tokenomics extraction
- Feature identification

### Content Generation
- Branded mascot integration
- Consistent style across all content
- Multiple content formats
- SEO-optimized text
- Engaging social media posts
- Educational videos

### Automation
- Scheduled content creation
- Batch processing
- Multi-project support
- Version control for all workflows
- Error handling and retry logic

## Version Control Strategy

**GitHub Repository:**
- Main branch: Production-ready code
- Develop branch: Integration branch
- Feature branches: Individual features/batches
- Workflow files version controlled
- Configuration templates included
- Sensitive data in .gitignore

## Cost Considerations

**Expected Monthly Costs (moderate usage):**
- LLM (GPT-4o-mini): ~$10-30/month
- Nano Banana API: TBD (check pricing)
- VEO3.1 API: TBD (check pricing)
- n8n hosting (if cloud): $20-50/month or free (self-hosted)

**Cost Optimization:**
- Use GPT-4o-mini for most text tasks
- Batch API requests when possible
- Cache research data to avoid re-scraping
- Local n8n hosting for development

## Next Steps

1. Initialize GitHub repository
2. Set up basic project structure
3. Begin Batch 1 development
4. Set up development environment

---

## Notes

- System uses local file storage for generated content
- Hybrid architecture leverages strengths of both n8n and Python
- Modular design allows independent development and testing of each service
- Scalable architecture can handle multiple projects simultaneously
