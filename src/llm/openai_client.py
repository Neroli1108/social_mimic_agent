"""OpenAI LLM client implementation."""
from typing import Optional
from openai import OpenAI

from .base import LLMClient
from ..config import settings


class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize OpenAI client.

        Args:
            model: The model to use (defaults to settings.openai_model).
            api_key: The API key (defaults to settings.openai_api_key).
        """
        self._model = model or settings.openai_model
        self._api_key = api_key or settings.openai_api_key
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        """Lazy load OpenAI client."""
        if self._client is None:
            if not self._api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
            self._client = OpenAI(api_key=self._api_key)
        return self._client

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "openai"

    @property
    def model_name(self) -> str:
        """Return the model name."""
        return self._model

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenAI API.

        Args:
            prompt: The input prompt.
            **kwargs: Additional parameters (temperature, max_tokens).

        Returns:
            The generated text response.
        """
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 500)

        response = self.client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content or ""
