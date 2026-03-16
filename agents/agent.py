from collections import deque
from typing import Optional

from src.llm.base import LLMClient
from src.config import settings


class Agent:
    def __init__(
        self,
        name: str,
        personality_traits: str,
        llm_client: Optional[LLMClient] = None,
        memory_limit: int = None
    ):
        self.name = name
        self.personality_traits = personality_traits
        self.llm_client = llm_client
        self.memory = deque(maxlen=memory_limit or settings.default_memory_limit)
        self.policy_knowledge = ""
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

    async def generate_response(self, prompt: str) -> str:
        """Generate a response using the injected LLM client."""
        if self.llm_client is not None:
            try:
                return await self.llm_client.generate(prompt)
            except Exception as e:
                print(f"LLM error for {self.name}: {e}")
                return self._fallback_response()
        else:
            return self._fallback_response()

    def _fallback_response(self) -> str:
        """Generate a fallback response when LLM is unavailable."""
        return (
            f"As {self.name}, with my {self.stance_on_policy} stance, "
            f"I respond to this situation with my {self.personality_traits} approach "
            f"in action #{self.action_count}."
        )

    def receive_policy(self, policy):
        self.policy_knowledge = policy
        self.log.append(f"Received policy: {policy}")
