import asyncio
from collections import deque
import openai

class Agent:
    def __init__(self, name, personality_traits, memory_limit=5):
        self.name = name
        self.personality_traits = personality_traits
        self.memory = deque(maxlen=memory_limit)
        self.policy_knowledge = ""
        self.log = []

    async def perceive(self, message):
        self.memory.append(message)
        self.log.append(f"Perceived: {message}")

    async def act(self):
        # Combine memory and personality to generate action
        prompt = f"""You are {self.name}, a person with {self.personality_traits}.
Policy: {self.policy_knowledge}
Memory: {list(self.memory)}
What do you do next?"""
        response = await self.generate_response(prompt)
        self.log.append(f"Acted: {response}")
        return response

    async def generate_response(self, prompt):
        # Use OpenAI API to generate a response
        openai.api_key = 'YOUR_API_KEY'
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message['content']

    def receive_policy(self, policy):
        self.policy_knowledge = policy
        self.log.append(f"Received policy update: {policy}")
