import unittest
import asyncio
from communication.communication import CommunicationSystem
from agents.agent import Agent

class TestCommunicationSystem(unittest.IsolatedAsyncioTestCase):
    async def test_broadcast(self):
        agent1 = Agent(name="Agent1", personality_traits="Trait1")
        agent2 = Agent(name="Agent2", personality_traits="Trait2")
        agents = [agent1, agent2]
        comm_system = CommunicationSystem(agents)

        await comm_system.broadcast(sender=agent1, message="Hello")

        self.assertIn("Agent1 says: Hello", agent2.memory)
        self.assertNotIn("Agent1 says: Hello", agent1.memory)

    async def test_send_policy(self):
        agent1 = Agent(name="Agent1", personality_traits="Trait1")
        agent2 = Agent(name="Agent2", personality_traits="Trait2")
        agents = [agent1, agent2]
        comm_system = CommunicationSystem(agents)

        class MockPolicy:
            policy_text = "Test Policy"

        policy = MockPolicy()
        comm_system.send_policy(policy)

        self.assertEqual(agent1.policy_knowledge, "Test Policy")
        self.assertEqual(agent2.policy_knowledge, "Test Policy")

if __name__ == '__main__':
    unittest.main()
