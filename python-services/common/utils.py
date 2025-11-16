"""Utility functions for the application."""
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
