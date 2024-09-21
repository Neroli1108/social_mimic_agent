import asyncio

class CommunicationSystem:
    def __init__(self, agents):
        self.agents = agents

    async def broadcast(self, sender, message):
        tasks = []
        for agent in self.agents:
            if agent != sender:
                tasks.append(agent.perceive(f"{sender.name} says: {message}"))
        await asyncio.gather(*tasks)

    async def send_policy(self, policy):
        tasks = [agent.receive_policy(policy.policy_text) for agent in self.agents]
        for agent in self.agents:
            agent.receive_policy(policy.policy_text)
