# agent.py
from collections import deque
import asyncio
from ..utils.llm_provider_selection import LLMProviderSelector
import google.generativeai as genai
from PIL import Image

class Agent:
    def __init__(self, name, personality_traits, provider, provider_model=None, memory_limit=5):
        self.name = name
        self.personality_traits = personality_traits
        self.memory = deque(maxlen=memory_limit)
        self.policy_knowledge = ""
        self.provider = provider
        self.provider_model = provider_model  # For Gemini and other multimodal providers
        self.log = []

    async def perceive(self, message):
        self.memory.append(message)
        self.log.append(f"Perceived: {message}")

    async def act(self):
        prompt = f"""You are {self.name}, a person with {self.personality_traits}.
Policy: {self.policy_knowledge}
Memory: {list(self.memory)}
What do you do next?"""
        response = await self.generate_response(prompt)
        self.log.append(f"Acted: {response}")
        return response

    async def generate_response(self, prompt):
        if self.provider == "openai":
            # Use OpenAI
            return "OpenAI-generated response"  # Placeholder for OpenAI response handling
        elif self.provider == "hugging_face":
            # Use Hugging Face
            return "Hugging Face-generated response"  # Placeholder for Hugging Face response handling
        elif self.provider == "gemini":
            # Handle multimodal input for Gemini
            model = self.provider_model
            response = model.generate_content(prompt)
            return response.text  # Text response from Gemini
        else:
            raise ValueError("Unknown provider.")

    def receive_policy(self, policy):
        self.policy_knowledge = policy
        self.log.append(f"Received policy update: {policy}")

