"""Prompt template management for content generation."""


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

    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render a template with variables.

        Args:
            template_name: Name of the template
            **kwargs: Template variables

        Returns:
            str: Rendered prompt
        """
        template = getattr(self, template_name, None)
        if not template:
            raise ValueError(f"Template not found: {template_name}")

        return template.format(**kwargs)
