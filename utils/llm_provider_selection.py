# llm_provider_selection.py
import google.generativeai as genai
import os

class LLMProviderSelector:
    def __init__(self):
        self.providers = {
            "OpenAI": self.openai_model,
            "Hugging Face": self.hugging_face_model,
            "Gemini": self.gemini_model  # New Gemini provider
        }
        self.gemini_variants = {
            "gemini-1.5-flash": "Fast and versatile performance",
            "gemini-1.5-flash-8b": "High volume and lower intelligence tasks",
            "gemini-1.5-pro": "Complex reasoning tasks",
            "gemini-1.0-pro": "Natural language and multi-turn tasks"
        }

    def list_providers(self):
        print("Available LLM providers:")
        for provider_name in self.providers:
            print(provider_name)

    def select_provider(self, provider_name):
        if provider_name in self.providers:
            return self.providers[provider_name]()
        else:
            raise ValueError(f"Provider {provider_name} is not available.")

    def openai_model(self):
        print("Using OpenAI GPT-4 model.")
        return "openai"

    def hugging_face_model(self):
        api_key = input("Please provide your Hugging Face API key: ")
        model_name = input("Enter the Hugging Face model name (e.g., gpt2, EleutherAI/gpt-neo-2.7B): ")
        
        return model_name, "hugging_face"

    def gemini_model(self):
        print("Available Gemini models:")
        for variant, description in self.gemini_variants.items():
            print(f"{variant}: {description}")

        selected_variant = input("Please select a Gemini model variant: ")
        if selected_variant not in self.gemini_variants:
            raise ValueError(f"Gemini model {selected_variant} is not available.")
        
        model = genai.GenerativeModel(selected_variant)
        return model, "gemini"

    def prompt_provider_selection(self):
        self.list_providers()
        selected_provider = input("Please select a provider: ")
        return self.select_provider(selected_provider)
