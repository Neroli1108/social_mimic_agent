import unittest
import os
from logging_system.logger import Logger
from agents.agent import Agent

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(log_dir='test_logs')
        self.agent = Agent(name="TestAgent", personality_traits="TestTrait")
        self.agent.log = ["Log Entry 1", "Log Entry 2"]

    def test_log_agent_activity(self):
        self.logger.log_agent_activity(self.agent)
        log_file = f"test_logs/{self.agent.name}.log"
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, 'r') as f:
            logs = f.read()
            self.assertIn("Log Entry 1", logs)
            self.assertIn("Log Entry 2", logs)
        # Clean up
        os.remove(log_file)
        os.rmdir('test_logs')

if __name__ == '__main__':
    unittest.main()
