"""Unified LLM client supporting multiple providers."""
from typing import Optional, List
import json
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


class LLMClient:
    """Unified LLM client supporting multiple providers."""

    def __init__(self, provider: str = "hermes", model: str = "Hermes-4-70B"):
        """
        Initialize LLM client.

        Args:
            provider: 'hermes', 'anthropic', or 'openai'
            model: Model name
        """
        self.provider = provider
        self.model = model
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == "openai":
            try:
                from openai import AsyncOpenAI
                import os
                self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                raise ImportError("Please install openai: pip install openai")
        elif self.provider == "anthropic":
            try:
                from anthropic import AsyncAnthropic
                import os
                self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except ImportError:
                raise ImportError("Please install anthropic: pip install anthropic")
        elif self.provider == "hermes":
            import os
            self.api_key = os.getenv("HERMES_API_KEY")
            self.base_url = os.getenv("HERMES_API_URL", "https://inference-api.nousresearch.com")
            if not self.api_key:
                raise ValueError("HERMES_API_KEY environment variable is required")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

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
        if self.provider == "openai":
            return await self._generate_openai(
                prompt, system_prompt, max_tokens, temperature, json_mode
            )
        elif self.provider == "anthropic":
            return await self._generate_anthropic(
                prompt, system_prompt, max_tokens, temperature
            )
        elif self.provider == "hermes":
            return await self._generate_hermes(
                prompt, system_prompt, max_tokens, temperature
            )

    async def _generate_openai(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int,
        temperature: float, json_mode: bool
    ) -> str:
        """Generate using OpenAI."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = await self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    async def _generate_anthropic(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int,
        temperature: float
    ) -> str:
        """Generate using Anthropic."""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = await self.client.messages.create(**kwargs)
        return response.content[0].text

    async def _generate_hermes(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int,
        temperature: float
    ) -> str:
        """Generate using Hermes API (Nous Research)."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

    def count_tokens(self, text: str) -> int:
        """Count tokens in text for cost estimation."""
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
