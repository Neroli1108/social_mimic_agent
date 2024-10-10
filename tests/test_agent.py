import unittest
from agents.agent import Agent
from collections import deque
import asyncio

class TestAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = Agent(name="TestAgent", personality_traits="test personality", memory_limit=3)

    async def test_perceive(self):
        await self.agent.perceive("Message 1")
        self.assertEqual(len(self.agent.memory), 1)
        self.assertIn("Message 1", self.agent.memory)

    async def test_memory_limit(self):
        await self.agent.perceive("Message 1")
        await self.agent.perceive("Message 2")
        await self.agent.perceive("Message 3")
        await self.agent.perceive("Message 4")
        self.assertEqual(len(self.agent.memory), 3)
        self.assertNotIn("Message 1", self.agent.memory)

    async def test_receive_policy(self):
        self.agent.receive_policy("Test Policy")
        self.assertEqual(self.agent.policy_knowledge, "Test Policy")

    async def test_act(self):
        # Mock generate_response to avoid API calls
        self.agent.generate_response = asyncio.coroutine(lambda x: "Test Action")
        action = await self.agent.act()
        self.assertEqual(action, "Test Action")

if __name__ == '__main__':
    unittest.main()
