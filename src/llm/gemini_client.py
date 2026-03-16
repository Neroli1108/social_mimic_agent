"""Gemini LLM client implementation."""
from typing import Optional
import google.generativeai as genai

from .base import LLMClient
from ..config import settings


class GeminiClient(LLMClient):
    """Google Gemini API client implementation."""

    GEMINI_VARIANTS = {
        "gemini-1.5-flash": "Fast and versatile performance",
        "gemini-1.5-flash-8b": "High volume and lower intelligence tasks",
        "gemini-1.5-pro": "Complex reasoning tasks",
        "gemini-1.0-pro": "Natural language and multi-turn tasks",
    }

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize Gemini client.

        Args:
            model: The model to use (defaults to settings.gemini_model).
            api_key: The API key (defaults to settings.gemini_api_key).
        """
        self._model = model or settings.gemini_model
        self._api_key = api_key or settings.gemini_api_key
        self._generative_model: Optional[genai.GenerativeModel] = None
        self._configured = False

    def _configure(self) -> None:
        """Configure the Gemini API."""
        if not self._configured:
            if not self._api_key:
                raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
            genai.configure(api_key=self._api_key)
            self._configured = True

    @property
    def generative_model(self) -> genai.GenerativeModel:
        """Lazy load Gemini GenerativeModel."""
        if self._generative_model is None:
            self._configure()
            self._generative_model = genai.GenerativeModel(self._model)
        return self._generative_model

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "gemini"

    @property
    def model_name(self) -> str:
        """Return the model name."""
        return self._model

    @classmethod
    def list_available_models(cls) -> dict:
        """Return available Gemini model variants."""
        return cls.GEMINI_VARIANTS.copy()

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Gemini API.

        Args:
            prompt: The input prompt.
            **kwargs: Additional parameters (not fully supported by Gemini).

        Returns:
            The generated text response.
        """
        response = self.generative_model.generate_content(prompt)
        return response.text.strip()
