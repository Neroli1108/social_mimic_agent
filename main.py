import asyncio
from agents.agent import Agent
from policies.policy import Policy
from communication.communication import CommunicationSystem
from logging_system.logger import Logger
from monitoring.monitor import Monitor
from utils.llm_provider_selection import LLMProviderSelector

async def main():
    # Select LLM provider
    selector = LLMProviderSelector()
    provider_model, provider = selector.prompt_provider_selection()

    # Initialize agents with LLM provider
    agent1 = Agent(name="Alice", personality_traits="optimistic and outgoing", provider=provider, provider_model=provider_model)
    agent2 = Agent(name="Bob", personality_traits="pessimistic and introverted", provider=provider, provider_model=provider_model)
    agents = [agent1, agent2]

    # Initialize systems
    policy = Policy("A new work-from-home policy is implemented.")
    comm_system = CommunicationSystem(agents)
    logger = Logger()
    monitor = Monitor(agents)

    # Send policy to agents
    await comm_system.send_policy(policy)

    # Simulation steps
    for _ in range(5):
        # Agents act
        actions = await asyncio.gather(*(agent.act() for agent in agents))

        # Agents communicate
        for agent, action in zip(agents, actions):
            await comm_system.broadcast(agent, action)

        # Log activities
        for agent in agents:
            logger.log_agent_activity(agent)

        # Monitor data
        monitor.collect_data()

    # Final report
    monitor.report()

if __name__ == "__main__":
    asyncio.run(main())
