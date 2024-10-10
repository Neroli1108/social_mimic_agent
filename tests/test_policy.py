import unittest
from policies.policy import Policy

class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.policy = Policy("Initial Policy")

    def test_update_policy(self):
        self.policy.update_policy("Updated Policy")
        self.assertEqual(self.policy.policy_text, "Updated Policy")

if __name__ == '__main__':
    unittest.main()
