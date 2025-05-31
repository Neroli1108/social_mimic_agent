import google.generativeai as genai
import os

class LLMProviderSelector:
    def __init__(self):
        self.providers = {
            "OpenAI": self.openai_model,
            "Hugging Face": self.hugging_face_model,
            "Gemini": self.gemini_model
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
            print(f"- {provider_name}")

    def select_provider(self, provider_name):
        # Make provider selection case-insensitive
        provider_name_normalized = None
        for key in self.providers.keys():
            if key.lower() == provider_name.lower():
                provider_name_normalized = key
                break
        
        if provider_name_normalized:
            return self.providers[provider_name_normalized]()
        else:
            available_providers = ", ".join(self.providers.keys())
            raise ValueError(f"Provider '{provider_name}' is not available. Available providers: {available_providers}")

    def openai_model(self):
        print("Using OpenAI GPT-4 model.")
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            api_key = input("Please provide your OpenAI API key: ")
        # You would set up OpenAI client here
        return None, "openai"

    def hugging_face_model(self):
        api_key = os.getenv('HUGGING_FACE_API_KEY')
        if not api_key:
            api_key = input("Please provide your Hugging Face API key (or press Enter to skip): ")
        model_name = input("Enter the Hugging Face model name (e.g., gpt2, EleutherAI/gpt-neo-2.7B): ")
        return model_name, "hugging_face"

    def gemini_model(self):
        # Set up Gemini API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            api_key = input("Please provide your Gemini API key: ")
            
        if api_key:
            try:
                genai.configure(api_key=api_key)
            except Exception as e:
                print(f"Error configuring Gemini API: {e}")
                return None, "gemini"
        
        print("Available Gemini models:")
        for variant, description in self.gemini_variants.items():
            print(f"- {variant}: {description}")

        selected_variant = input("Please select a Gemini model variant (or press Enter for gemini-1.5-flash): ")
        if not selected_variant:
            selected_variant = "gemini-1.5-flash"
            
        if selected_variant not in self.gemini_variants:
            print(f"Warning: {selected_variant} not in predefined variants, but attempting to use it...")
        
        try:
            model = genai.GenerativeModel(selected_variant)
            print(f"Successfully initialized Gemini model: {selected_variant}")
            return model, "gemini"
        except Exception as e:
            print(f"Error creating Gemini model: {e}")
            return None, "gemini"

    def prompt_provider_selection(self):
        self.list_providers()
        selected_provider = input("Please select a provider (OpenAI/Hugging Face/Gemini): ").strip()
        return self.select_provider(selected_provider)