import asyncio

class CommunicationSystem:
    def __init__(self, agents):
        self.agents = agents

    async def broadcast(self, sender, message):
        print(f"   📡 {sender.name} broadcasting message to {len(self.agents) - 1} other agents...")
        tasks = []
        for agent in self.agents:
            if agent != sender:
                tasks.append(agent.perceive(f"{sender.name} says: {message}"))
                print(f"      → Message sent to {agent.name}")
        if tasks:
            await asyncio.gather(*tasks)

    async def send_policy(self, policy):
        print(f"📋 Sending policy to all {len(self.agents)} agents...")
        for agent in self.agents:
            agent.receive_policy(policy.policy_text)
            print(f"   ✓ Policy sent to {agent.name}")
        print(f"✅ Policy distribution complete: '{policy.policy_text}'")