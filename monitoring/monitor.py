class Monitor:
    def __init__(self, agents):
        self.agents = agents
        self.data = []
        self.step_count = 0

    def collect_data(self):
        step_data = {
            'step': self.step_count,
            'timestamp': self.get_timestamp(),
            'agents': []
        }
        
        for agent in self.agents:
            agent_data = {
                'name': agent.name,
                'personality': agent.personality_traits,
                'memory_count': len(agent.memory),
                'latest_memory': list(agent.memory)[-1] if agent.memory else "No recent activity",
                'policy_knowledge': agent.policy_knowledge,
                'total_actions': len(agent.log)
            }
            step_data['agents'].append(agent_data)
        
        self.data.append(step_data)
        self.step_count += 1
        
    def print_step_summary(self, step_data):
        print(f"\n{'='*60}")
        print(f"SIMULATION STEP {step_data['step'] + 1} - {step_data['timestamp']}")
        print(f"{'='*60}")
        
        for agent_data in step_data['agents']:
            print(f"\n📋 AGENT: {agent_data['name']}")
            print(f"   Personality: {agent_data['personality']}")
            print(f"   Memory Items: {agent_data['memory_count']}")
            print(f"   Total Actions: {agent_data['total_actions']}")
            
            # Show latest memory with proper formatting
            if agent_data['latest_memory'] != "No recent activity":
                latest = agent_data['latest_memory']
                if len(latest) > 100:
                    latest = latest[:97] + "..."
                print(f"   Latest Activity: {latest}")
            else:
                print(f"   Latest Activity: {agent_data['latest_memory']}")
                
        print(f"\n{'-'*60}")

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def report(self):
        if not self.data:
            print("No monitoring data collected.")
            return
            
        print(f"\n{'🔍 FINAL SIMULATION REPORT':^60}")
        print(f"{'='*60}")
        print(f"Total Steps: {len(self.data)}")
        print(f"Simulation Duration: {self.data[0]['timestamp']} to {self.data[-1]['timestamp']}")
        
        # Agent summary
        for agent in self.agents:
            print(f"\n📊 {agent.name.upper()} SUMMARY:")
            print(f"   Personality: {agent.personality_traits}")
            print(f"   Final Memory Count: {len(agent.memory)}")
            print(f"   Total Actions Taken: {len(agent.log)}")
            print(f"   Policy Understanding: {'✓' if agent.policy_knowledge else '✗'}")
            
        # Clear data after reporting
        self.data = []