"""Manage brand style and mascot consistency."""
from typing import Dict, Optional
import json


class StyleManager:
    """Manage brand style and mascot consistency."""

    def __init__(self, brand_config_path: str = None):
        """
        Load brand configuration.

        Args:
            brand_config_path: Path to brand configuration JSON
        """
        self.brand_config = self._load_config(brand_config_path) if brand_config_path else self._default_config()

    def _load_config(self, config_path: str) -> dict:
        """Load brand configuration from file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            return self._default_config()

    def _default_config(self) -> dict:
        """Default brand configuration."""
        return {
            'mascot': {
                'name': 'CryptoBuddy',
                'description': 'Friendly cartoon character',
                'emotions': ['happy', 'excited', 'thinking', 'surprised']
            },
            'colors': ['#3B82F6', '#8B5CF6', '#EC4899'],
            'style': 'modern digital art, vibrant colors, clean design'
        }

    def apply_brand_style(self, base_prompt: str, include_mascot: bool = True) -> str:
        """
        Enhance prompt with brand elements.

        Args:
            base_prompt: Basic image description
            include_mascot: Whether to include mascot

        Returns:
            str: Enhanced prompt with brand style
        """
        enhanced = base_prompt

        if include_mascot:
            mascot_desc = self.get_mascot_prompt()
            enhanced = f"{enhanced}, with {mascot_desc}"

        enhanced += f", {self.brand_config['style']}"
        return enhanced

    def get_mascot_prompt(self, emotion: str = "happy", action: str = None) -> str:
        """
        Generate consistent mascot description.

        Args:
            emotion: 'happy', 'excited', 'thinking', 'surprised'
            action: Specific action mascot is doing

        Returns:
            str: Detailed mascot description for consistency
        """
        mascot = self.brand_config['mascot']
        desc = f"{mascot['name']}, {mascot['description']}, {emotion} expression"

        if action:
            desc += f", {action}"

        return desc

    def get_style_preset(self, content_type: str) -> dict:
        """
        Get style configuration for content type.

        Args:
            content_type: 'social_media', 'infographic', 'header', 'announcement'

        Returns:
            dict: Style configuration
        """
        presets = {
            'social_media': {
                'aspect_ratio': '1:1',
                'style_keywords': ['clean', 'modern', 'engaging'],
                'color_scheme': 'vibrant',
                'composition': 'centered'
            },
            'infographic': {
                'aspect_ratio': '4:5',
                'style_keywords': ['informative', 'clear', 'professional'],
                'color_scheme': 'balanced',
                'composition': 'structured'
            },
            'announcement': {
                'aspect_ratio': '16:9',
                'style_keywords': ['bold', 'eye-catching', 'exciting'],
                'color_scheme': 'dramatic',
                'composition': 'dynamic'
            }
        }

        return presets.get(content_type, presets['social_media'])
