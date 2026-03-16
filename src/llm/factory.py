"""Factory for creating LLM clients."""
from typing import Optional

from .base import LLMClient
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .huggingface_client import HuggingFaceClient
from ..config import settings


PROVIDERS = {
    "openai": OpenAIClient,
    "gemini": GeminiClient,
    "huggingface": HuggingFaceClient,
}


def create_llm_client(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> LLMClient:
    """Factory function to create an LLM client based on provider.

    Args:
        provider: The LLM provider name (openai, gemini, huggingface).
                  Defaults to settings.llm_provider.
        model: Optional model override.
        api_key: Optional API key override.
        **kwargs: Additional arguments passed to the client constructor.

    Returns:
        An instance of the appropriate LLMClient subclass.

    Raises:
        ValueError: If the provider is unknown.
    """
    provider = (provider or settings.llm_provider).lower()

    if provider not in PROVIDERS:
        available = ", ".join(PROVIDERS.keys())
        raise ValueError(f"Unknown provider: '{provider}'. Available providers: {available}")

    client_class = PROVIDERS[provider]
    return client_class(model=model, api_key=api_key, **kwargs)


def list_providers() -> list[str]:
    """Return a list of available provider names."""
    return list(PROVIDERS.keys())
