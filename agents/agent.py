from collections import deque
import asyncio
import google.generativeai as genai
import os
import random

class Agent:
    def __init__(self, name, personality_traits, provider=None, provider_model=None, memory_limit=5):
        self.name = name
        self.personality_traits = personality_traits
        self.memory = deque(maxlen=memory_limit)
        self.policy_knowledge = ""
        self.provider = provider
        self.provider_model = provider_model
        self.log = []
        self.action_count = 0
        self.stance_on_policy = None  # Will be determined based on personality

    async def perceive(self, message):
        self.memory.append(message)
        self.log.append(f"Perceived: {message[:50]}{'...' if len(message) > 50 else ''}")

    async def act(self):
        # Add more variation to actions based on step count and memory
        self.action_count += 1
        
        # Determine stance if not set
        if self.stance_on_policy is None:
            self.stance_on_policy = self._determine_policy_stance()
        
        # Create more dynamic prompts
        context = self._build_context()
        prompt = f"""You are {self.name}, a person with {self.personality_traits} personality.

Policy: {self.policy_knowledge}
Your stance on this policy: {self.stance_on_policy}
Current situation: This is action #{self.action_count} in our ongoing community discussion.
Recent community interactions: {context}

Based on your personality, stance, and the evolving situation, what SPECIFIC action do you take next? 
Be concrete and varied - don't repeat the same action. Consider:
- Different ways to express your stance
- Various community engagement methods
- Personal preparations or reactions
- Interactions with specific people or groups

Respond in 1-2 sentences describing a DIFFERENT action from before."""

        response = await self.generate_response(prompt)
        self.log.append(f"Acted: {response}")
        return response

    def _determine_policy_stance(self):
        """Determine agent's stance on policy based on personality and policy type"""
        personality_lower = self.personality_traits.lower()
        policy_lower = self.policy_knowledge.lower()
        
        # Analyze policy type
        if "tariff" in policy_lower:
            if any(trait in personality_lower for trait in ["conservative", "traditional", "business"]):
                return "cautiously supportive - believes it protects local industry"
            elif any(trait in personality_lower for trait in ["progressive", "community-minded", "social"]):
                return "concerned - worried about increased costs for families"
            else:
                return "neutral but seeking more information"
        elif "work-from-home" in policy_lower:
            if any(trait in personality_lower for trait in ["progressive", "flexible", "adaptive"]):
                return "very supportive - sees benefits for work-life balance"
            elif any(trait in personality_lower for trait in ["traditional", "conservative"]):
                return "skeptical - prefers traditional office structure"
            else:
                return "cautiously optimistic - needs to see implementation details"
        else:
            # Generic policy stance
            if any(trait in personality_lower for trait in ["optimistic", "progressive", "supportive"]):
                return "generally supportive with some reservations"
            elif any(trait in personality_lower for trait in ["pessimistic", "conservative", "cautious"]):
                return "skeptical and wants more information"
            else:
                return "neutral - waiting to see impacts"

    def _build_context(self):
        """Build context from recent memories"""
        if not self.memory:
            return "No recent interactions"
        
        recent_memories = list(self.memory)[-2:] if len(self.memory) >= 2 else list(self.memory)
        return "; ".join([mem[:80] + "..." if len(mem) > 80 else mem for mem in recent_memories])

    async def generate_response(self, prompt):
        if self.provider == "openai":
            return f"As {self.name}, given my {self.stance_on_policy} stance, I take action #{self.action_count} to address this tariff policy in my own way."
        elif self.provider == "hugging_face":
            return f"With my {self.personality_traits} nature and {self.stance_on_policy} position, I respond to this policy change strategically."
        elif self.provider == "gemini":
            try:
                if self.provider_model:
                    response = self.provider_model.generate_content(prompt)
                    return response.text.strip()
                else:
                    return f"As {self.name}, being {self.stance_on_policy}, I take concrete action #{self.action_count} regarding the tariff policy."
            except Exception as e:
                print(f"⚠️  Gemini API error for {self.name}: {e}")
                return f"As {self.name}, with my {self.stance_on_policy} stance, I respond to this policy in action #{self.action_count}."
        else:
            return f"As {self.name}, I respond to this situation with my {self.personality_traits} approach in action #{self.action_count}."

    def receive_policy(self, policy):
        self.policy_knowledge = policy
        self.log.append(f"Received policy: {policy}")