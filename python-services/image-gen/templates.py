"""Image generation templates."""
from typing import Dict


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
            dict: Prompt and configuration
        """
        if template_name not in self.TEMPLATES:
            raise ValueError(f"Template not found: {template_name}")

        template = self.TEMPLATES[template_name]
        prompt = template['prompt_template'].format(**variables)

        return {
            'prompt': prompt,
            'aspect_ratio': template['aspect_ratio'],
            'style_config': {
                'structure': template['structure']
            }
        }

    def create_custom_template(
        self,
        name: str,
        structure: str,
        prompt_template: str,
        aspect_ratio: str = "1:1"
    ) -> None:
        """
        Add custom template to library.

        Args:
            name: Template name
            structure: Visual structure description
            prompt_template: Template string with variables
            aspect_ratio: Image aspect ratio
        """
        self.TEMPLATES[name] = {
            'aspect_ratio': aspect_ratio,
            'structure': structure,
            'prompt_template': prompt_template
        }
