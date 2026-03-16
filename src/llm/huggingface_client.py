"""HuggingFace LLM client implementation."""
from typing import Optional
import requests

from .base import LLMClient
from ..config import settings


class HuggingFaceClient(LLMClient):
    """HuggingFace Inference API client implementation."""

    API_URL_TEMPLATE = "https://api-inference.huggingface.co/models/{model}"

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize HuggingFace client.

        Args:
            model: The model to use (defaults to settings.huggingface_model).
            api_key: The API key (defaults to settings.huggingface_api_key).
        """
        self._model = model or settings.huggingface_model
        self._api_key = api_key or settings.huggingface_api_key

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "huggingface"

    @property
    def model_name(self) -> str:
        """Return the model name."""
        return self._model

    @property
    def _headers(self) -> dict:
        """Return API headers."""
        if not self._api_key:
            raise ValueError("HuggingFace API key is required. Set HUGGINGFACE_API_KEY environment variable.")
        return {"Authorization": f"Bearer {self._api_key}"}

    @property
    def _api_url(self) -> str:
        """Return the API URL for the configured model."""
        if not self._model:
            raise ValueError("HuggingFace model name is required. Set HUGGINGFACE_MODEL environment variable.")
        return self.API_URL_TEMPLATE.format(model=self._model)

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using HuggingFace Inference API.

        Args:
            prompt: The input prompt.
            **kwargs: Additional parameters (max_length, temperature).

        Returns:
            The generated text response.
        """
        max_length = kwargs.get("max_tokens", 500)
        temperature = kwargs.get("temperature", 0.7)

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "return_full_text": False,
            }
        }

        response = requests.post(
            self._api_url,
            headers=self._headers,
            json=payload
        )
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return str(result)
