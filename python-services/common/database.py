"""Database models and operations using SQLAlchemy."""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import settings

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
