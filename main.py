import asyncio
import time

from agents.agent import Agent
from policies.policy import Policy
from communication.communication import CommunicationSystem
from monitoring.monitor import Monitor
from logging_system.logger import Logger
from utils.scenario_generator import ScenarioGenerator
from utils.policy_evaluator import PolicyEvaluator

from src.config import settings
from src.llm import create_llm_client, list_providers, LLMClient
from src.llm.gemini_client import GeminiClient


class SimulationManager:
    def __init__(self):
        self.agents = []
        self.scenario_generator = ScenarioGenerator()
        self.policy_evaluator = PolicyEvaluator()
        self.comm_system = None
        self.monitor = None
        self.logger = None
        self.llm_client: LLMClient = None

    def select_llm_provider(self) -> LLMClient:
        """Select and configure LLM provider using the factory pattern."""
        print("\n Available LLM providers:")
        providers = list_providers()
        for i, provider in enumerate(providers, 1):
            print(f"{i}. {provider.title()}")

        choice = input(f"\nSelect provider (1-{len(providers)}, default=2 for Gemini): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(providers):
                selected_provider = providers[idx]
            else:
                selected_provider = "gemini"
        except ValueError:
            selected_provider = "gemini"

        print(f"\nSelected provider: {selected_provider.title()}")

        # Handle model selection for Gemini
        model = None
        if selected_provider == "gemini":
            variants = GeminiClient.list_available_models()
            print("\nAvailable Gemini models:")
            variant_list = list(variants.items())
            for i, (name, desc) in enumerate(variant_list, 1):
                print(f"{i}. {name}: {desc}")

            model_choice = input(f"\nSelect model (1-{len(variant_list)}, default=1): ").strip()
            try:
                model_idx = int(model_choice) - 1
                if 0 <= model_idx < len(variant_list):
                    model = variant_list[model_idx][0]
                else:
                    model = settings.gemini_model
            except ValueError:
                model = settings.gemini_model

        # Check for API key
        api_key = None
        if selected_provider == "openai" and not settings.openai_api_key:
            api_key = input("Enter your OpenAI API key: ").strip()
        elif selected_provider == "gemini" and not settings.gemini_api_key:
            api_key = input("Enter your Gemini API key: ").strip()
        elif selected_provider == "huggingface":
            if not settings.huggingface_api_key:
                api_key = input("Enter your HuggingFace API key: ").strip()
            if not model and not settings.huggingface_model:
                model = input("Enter the HuggingFace model name (e.g., gpt2): ").strip()

        try:
            client = create_llm_client(provider=selected_provider, model=model, api_key=api_key)
            print(f" Successfully initialized {client.provider_name.title()} with model: {client.model_name}")
            return client
        except Exception as e:
            print(f" Error initializing {selected_provider}: {e}")
            print("Falling back to Gemini...")
            return create_llm_client(provider="gemini")

    def get_user_policy(self):
        """Get policy input from user with polishing option"""
        print("\n POLICY CONFIGURATION")
        print("="*50)

        use_custom = input("Would you like to enter a custom policy? (y/n, default=n): ").strip().lower()

        if use_custom == 'y':
            print("\nPlease enter your policy:")
            print("(You can describe any new rule, regulation, or change you want to implement)")
            raw_policy = input("Policy: ").strip()

            if not raw_policy:
                policy_text = "A new work-from-home policy is implemented."
                print(f"Using default policy: {policy_text}")
            else:
                # Polish the policy
                polished_result = self.scenario_generator.polish_custom_policy(raw_policy)

                print(f"\n POLICY ENHANCEMENT:")
                print(f"Original: {polished_result['original']}")
                print(f"Enhanced: {polished_result['polished']}")
                print(f"\nPolicy Analysis:")
                analysis = polished_result['analysis']
                print(f"  Type: {analysis['type']}")
                print(f"  Scope: {analysis['scope']}")
                print(f"  Impact Areas: {', '.join(analysis['impact_areas'])}")
                print(f"  Key Stakeholders: {', '.join(analysis['stakeholders'])}")
                print(f"  Complexity: {analysis['complexity']}")

                if polished_result['suggestions']:
                    print(f"\n Suggestions for improvement:")
                    for suggestion in polished_result['suggestions']:
                        print(f"  * {suggestion}")

                accept_enhanced = input(f"\nUse the enhanced version? (y/n, default=y): ").strip().lower()
                policy_text = polished_result['polished'] if accept_enhanced != 'n' else polished_result['original']
        else:
            # Provide example policies
            example_policies = [
                "A new work-from-home policy is implemented.",
                "The city introduces a 25% increase in property taxes to fund infrastructure improvements.",
                "A mandatory digital detox weekend is announced for all employees.",
                "The government implements a 40% tariff on imported goods.",
                "A new environmental sustainability initiative requiring 50% waste reduction is launched."
            ]

            print("\nAvailable example policies:")
            for i, policy in enumerate(example_policies, 1):
                print(f"{i}. {policy}")

            choice = input(f"\nSelect a policy (1-{len(example_policies)}) or press Enter for default: ").strip()

            try:
                policy_text = example_policies[int(choice) - 1]
            except (ValueError, IndexError):
                policy_text = example_policies[0]

        return policy_text

    def get_scenario_and_agents(self):
        """Get scenario and agent configuration from user with custom scenario polishing"""
        print("\n SCENARIO & AGENT CONFIGURATION")
        print("="*50)

        # Get scenario
        scenario_options = self.scenario_generator.get_scenario_options()
        print("Available scenarios:")
        for i, scenario in enumerate(scenario_options, 1):
            info = self.scenario_generator.get_scenario_info(scenario)
            print(f"{i}. {scenario.title()}: {info['description']}")

        print(f"{len(scenario_options) + 1}. Custom scenario")

        scenario_choice = input(f"\nSelect scenario (1-{len(scenario_options) + 1}): ").strip()

        try:
            choice_idx = int(scenario_choice) - 1
            if choice_idx < len(scenario_options):
                selected_scenario = scenario_options[choice_idx]
                scenario_info = self.scenario_generator.get_scenario_info(selected_scenario)
                print(f"\n Selected: {selected_scenario.title()}")
                print(f"Context: {scenario_info['context']}")
                custom_description = None
            else:
                selected_scenario = "custom"
                raw_description = input("Describe your custom scenario: ").strip()
                if not raw_description:
                    raw_description = "A general social environment with diverse individuals"

                # Polish the custom scenario
                polished_result = self.scenario_generator.polish_custom_scenario(raw_description)

                print(f"\n SCENARIO ENHANCEMENT:")
                print(f"Original: {polished_result['original']}")
                print(f"Enhanced: {polished_result['polished']}")

                if polished_result['suggestions']:
                    print(f"\n Suggestions for improvement:")
                    for suggestion in polished_result['suggestions']:
                        print(f"  * {suggestion}")

                accept_enhanced = input(f"\nUse the enhanced version? (y/n, default=y): ").strip().lower()
                custom_description = polished_result['polished'] if accept_enhanced != 'n' else polished_result['original']
                print(f"\n Custom scenario: {custom_description}")
        except (ValueError, IndexError):
            selected_scenario = "workplace"
            scenario_info = self.scenario_generator.get_scenario_info(selected_scenario)
            custom_description = None
            print(f"\n Using default: {selected_scenario.title()}")

        # Get number of agents
        max_agents = settings.max_agents
        while True:
            try:
                num_agents = int(input(f"\nHow many agents do you want? (2-{max_agents}, default=3): ") or "3")
                if 2 <= num_agents <= max_agents:
                    break
                else:
                    print(f"Please enter a number between 2 and {max_agents}.")
            except ValueError:
                print("Please enter a valid number.")

        # Generate or get personalities
        if selected_scenario == "custom":
            suggested_personalities = self.scenario_generator.analyze_custom_scenario(custom_description)
        else:
            scenario_info = self.scenario_generator.get_scenario_info(selected_scenario)
            suggested_personalities = scenario_info['sample_personalities']

        # Create agents with personalities
        agent_names = self.scenario_generator.generate_agent_names(num_agents, selected_scenario)
        agents_config = []

        print(f"\n AGENT PERSONALITY ASSIGNMENT")
        print("-" * 40)

        for i in range(num_agents):
            print(f"\nAgent {i+1}: {agent_names[i]}")

            if i < len(suggested_personalities):
                suggested = suggested_personalities[i]
                print(f"Suggested personality: {suggested}")

                accept = input("Accept this personality? (y/n/custom, default=y): ").strip().lower()

                if accept == 'n' or accept == 'custom':
                    print("\nPersonality guidelines:")
                    print("- Use 2-3 descriptive traits (e.g., 'optimistic and outgoing')")
                    print("- Consider traits like: analytical, creative, social, cautious, ambitious, empathetic")
                    print("- Make each agent unique for better simulation diversity")

                    custom_personality = input("Enter custom personality: ").strip()
                    personality = custom_personality if custom_personality else suggested
                else:
                    personality = suggested
            else:
                print("No suggestion available.")
                personality = input("Enter personality traits: ").strip()
                if not personality:
                    personality = "balanced and adaptable"

            agents_config.append({
                'name': agent_names[i],
                'personality': personality
            })

            print(f" {agent_names[i]}: {personality}")

        # Final confirmation
        print(f"\n AGENT SUMMARY:")
        for config in agents_config:
            print(f"  - {config['name']}: {config['personality']}")

        confirm = input("\nConfirm these agents? (y/n, default=y): ").strip().lower()
        if confirm == 'n':
            print("Restarting agent configuration...")
            return self.get_scenario_and_agents()  # Recursive call to restart

        return agents_config, selected_scenario

    def create_agents(self, agents_config):
        """Create agent instances with injected LLM client"""
        self.agents = []
        for config in agents_config:
            agent = Agent(
                name=config['name'],
                personality_traits=config['personality'],
                llm_client=self.llm_client
            )
            self.agents.append(agent)

        print(f"\n Created {len(self.agents)} agents successfully!")

    def get_simulation_mode(self):
        """Get simulation execution mode from user"""
        print("\n SIMULATION EXECUTION MODE")
        print("="*50)
        print("1. Step-by-step (pause after each step for review)")
        print("2. Continuous (run all steps at once)")

        choice = input("Select mode (1/2, default=1): ").strip()
        return choice != '2'  # Return True for step-by-step, False for continuous

    async def run_simulation_step(self, step, total_steps):
        """Run a single simulation step"""
        print(f"\n Processing step {step + 1}/{total_steps}...")

        # Each agent acts
        for agent in self.agents:
            print(f"    {agent.name} is thinking...")
            action = await agent.act()
            print(f"    {agent.name}: {action[:100]}{'...' if len(action) > 100 else ''}")

            # Broadcast action to other agents
            await self.comm_system.broadcast(agent, action)

        # Collect monitoring data
        self.monitor.collect_data()

        # Print step summary
        if self.monitor.data:
            self.monitor.print_step_summary(self.monitor.data[-1])

        # Log agent activities
        for agent in self.agents:
            self.logger.log_agent_activity(agent)

    async def run_simulation(self, policy_text):
        """Run the main simulation with enhanced evaluation"""
        # Configure evaluation rules before starting simulation
        print(f"\n Configuring evaluation system...")
        self.policy_evaluator.configure_evaluation_rules()

        # Initialize systems
        print(f"\n Initializing simulation systems...")
        policy = Policy(policy_text)
        self.comm_system = CommunicationSystem(self.agents)
        self.monitor = Monitor(self.agents)
        self.logger = Logger()

        print(f" Policy: {policy.policy_text}")
        print(f" Communication system ready")
        print(f" Monitoring system ready")
        print(f" Logging system ready")

        # Send policy to agents
        print(f"\n Distributing policy to agents...")
        await self.comm_system.send_policy(policy)

        # Get simulation mode
        step_by_step = self.get_simulation_mode()

        # Get number of simulation steps
        while True:
            try:
                simulation_steps = int(input(f"\nNumber of simulation steps (1-20, default=5): ") or "5")
                if 1 <= simulation_steps <= 20:
                    break
                else:
                    print("Please enter a number between 1 and 20.")
            except ValueError:
                print("Please enter a valid number.")

        if not step_by_step:
            input("\nPress Enter to start simulation...")

        print(f"\n Running {simulation_steps} simulation steps...")

        # Run simulation steps
        for step in range(simulation_steps):
            await self.run_simulation_step(step, simulation_steps)

            if step_by_step and step < simulation_steps - 1:
                print(f"\n{'='*60}")
                continue_choice = input(f"Continue to step {step + 2}? (y/n/auto, default=y): ").strip().lower()
                if continue_choice == 'n':
                    print("Simulation stopped by user.")
                    break
                elif continue_choice == 'auto':
                    print("Switching to continuous mode...")
                    step_by_step = False
            elif not step_by_step:
                time.sleep(0.5)  # Small delay for readability

        # Generate evaluation report with custom rules
        print(f"\n Simulation completed! Generating evaluation report...")
        evaluation = self.policy_evaluator.evaluate_policy_impact(self.agents, self.monitor.data, policy_text)
        self.policy_evaluator.print_evaluation_report(evaluation)

        # Final monitoring report
        print(f"\n DETAILED SIMULATION REPORT:")
        self.monitor.report()

        print(f"\n Log files created in 'logs/' directory:")
        for agent in self.agents:
            print(f"   - logs/{agent.name}.log")


async def main():
    print(" Starting Enhanced Social Mimic Agent System...")
    print("="*60)

    sim_manager = SimulationManager()

    # Initialize LLM Provider using factory pattern
    print("\n LLM PROVIDER SELECTION")
    print("="*50)
    sim_manager.llm_client = sim_manager.select_llm_provider()

    # Get policy from user
    policy_text = sim_manager.get_user_policy()

    # Get scenario and agents configuration
    agents_config, scenario = sim_manager.get_scenario_and_agents()

    # Create agents
    sim_manager.create_agents(agents_config)

    # Run simulation
    await sim_manager.run_simulation(policy_text)

    # Ask if user wants to run another simulation
    print(f"\n Would you like to run another simulation?")
    another = input("Run again? (y/n, default=n): ").strip().lower()
    if another == 'y':
        print("\n" + "="*60)
        await main()  # Recursive call for another simulation


if __name__ == "__main__":
    asyncio.run(main())
