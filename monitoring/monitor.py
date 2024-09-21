class Monitor:
    def __init__(self, agents):
        self.agents = agents
        self.data = []

    def collect_data(self):
        for agent in self.agents:
            self.data.append({
                'name': agent.name,
                'memory': list(agent.memory),
                'policy_knowledge': agent.policy_knowledge
            })

    def report(self):
        # For simplicity, just print the data
        for datum in self.data:
            print(datum)
        self.data.clear()
