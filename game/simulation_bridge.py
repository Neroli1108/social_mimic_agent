"""Bridges backend simulation with Pygame UI using threading + queue."""
import asyncio
import threading
import queue
import time

from agents.agent import Agent
from policies.policy import Policy
from communication.communication import CommunicationSystem
from monitoring.monitor import Monitor
from logging_system.logger import Logger
from utils.policy_evaluator import PolicyEvaluator
from src.llm.factory import create_llm_client


class SimulationBridge:
    def __init__(self):
        self.event_queue = queue.Queue()
        self._thread = None
        self.agents = []
        self.is_running = False
        self.is_complete = False
        self.evaluation = None

    def start(self, config: dict):
        """
        config keys: provider, model, api_key, policy, scenario,
                     agents (list of {name, personality}),
                     steps (int), evaluation_criteria (dict, optional)
        """
        self.is_running = True
        self.is_complete = False
        self._thread = threading.Thread(target=self._run, args=(config,), daemon=True)
        self._thread.start()

    def _run(self, config):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._simulate(config))
        except Exception as e:
            self.event_queue.put(('error', str(e)))
        finally:
            self.is_running = False
            self.is_complete = True
            loop.close()

    async def _simulate(self, config):
        # Init LLM
        try:
            llm = create_llm_client(
                provider=config.get('provider', 'gemini'),
                model=config.get('model') or None,
                api_key=config.get('api_key') or None,
            )
            self.event_queue.put(('log', f'LLM initialized: {config.get("provider", "gemini")}', 'cyan'))
        except Exception as e:
            self.event_queue.put(('error', f'LLM init failed: {e}'))
            return

        # Create agents
        self.agents = []
        for ac in config['agents']:
            a = Agent(
                name=ac['name'],
                personality_traits=ac['personality'],
                llm_client=llm,
            )
            self.agents.append(a)
        self.event_queue.put((
            'agents_ready',
            [{'name': a.name, 'personality': a.personality_traits} for a in self.agents],
        ))

        # Create systems
        policy = Policy(config['policy'])
        comm = CommunicationSystem(self.agents)
        monitor = Monitor(self.agents)
        logger = Logger()

        # Distribute policy
        await comm.send_policy(policy)
        self.event_queue.put(('log', 'Policy distributed to all agents', 'cyan'))

        steps = config.get('steps', 5)
        for step in range(steps):
            self.event_queue.put(('step_start', {'step': step, 'total': steps}))

            for agent in self.agents:
                self.event_queue.put(('agent_thinking', agent.name))
                action = await agent.act()
                self.event_queue.put(('agent_action', {
                    'name': agent.name,
                    'action': action,
                    'stance': agent.stance_on_policy,
                    'step': step,
                }))
                await comm.broadcast(agent, action)
                self.event_queue.put(('broadcast', {
                    'from': agent.name,
                    'to': [a.name for a in self.agents if a != agent],
                    'message': action[:80],
                }))
                await asyncio.sleep(0.1)

            monitor.collect_data()
            logger_data = [{'name': a.name, 'stance': a.stance_on_policy} for a in self.agents]
            self.event_queue.put(('step_complete', {
                'step': step,
                'total': steps,
                'agents': logger_data,
            }))
            for agent in self.agents:
                logger.log_agent_activity(agent)

        # Evaluate
        evaluator = PolicyEvaluator()
        evaluator.active_criteria = (
            config.get('evaluation_criteria') or evaluator.rules_manager.default_criteria
        )
        evaluation = evaluator.evaluate_policy_impact(
            self.agents, monitor.data, config['policy']
        )
        self.evaluation = evaluation
        self.event_queue.put(('evaluation_ready', evaluation))

    def poll(self):
        """Return list of all pending events."""
        events = []
        while True:
            try:
                events.append(self.event_queue.get_nowait())
            except queue.Empty:
                break
        return events
