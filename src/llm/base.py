"""Abstract base class for LLM clients."""
from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """Abstract base class for LLM provider clients."""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt to send to the LLM.
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            The generated text response.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the provider."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the model being used."""
        pass
