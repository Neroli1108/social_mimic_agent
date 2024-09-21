import unittest
from monitoring.monitor import Monitor
from agents.agent import Agent

class TestMonitor(unittest.TestCase):
    def setUp(self):
        agent1 = Agent(name="Agent1", personality_traits="Trait1")
        agent2 = Agent(name="Agent2", personality_traits="Trait2")
        self.agents = [agent1, agent2]
        self.monitor = Monitor(self.agents)

    def test_collect_data(self):
        self.monitor.collect_data()
        self.assertEqual(len(self.monitor.data), 2)
        self.assertEqual(self.monitor.data[0]['name'], "Agent1")
        self.assertEqual(self.monitor.data[1]['name'], "Agent2")

    def test_report(self):
        self.monitor.collect_data()
        # Capture the output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.monitor.report()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Agent1", output)
        self.assertIn("Agent2", output)
        self.assertEqual(len(self.monitor.data), 0)  # Data should be cleared after report

if __name__ == '__main__':
    unittest.main()
