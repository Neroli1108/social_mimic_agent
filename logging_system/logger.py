import os

class Logger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log_agent_activity(self, agent):
        with open(f"{self.log_dir}/{agent.name}.log", 'a') as f:
            for entry in agent.log:
                f.write(entry + '\n')
        agent.log.clear()
