import unittest
from lead_router import score_lead

class TestLeadRouter(unittest.TestCase):
    def test_hot_lead(self):
        d = score_lead({
            "name": "A",
            "email": "a@example.com",
            "budget": 1500,
            "timeline_days": 3,
            "service": "API integration",
            "message": "Need CRM automation"
        })
        self.assertEqual(d.tier, "HOT")
        self.assertGreaterEqual(d.score, 70)

    def test_warm_lead(self):
        d = score_lead({
            "name": "B",
            "email": "b@example.com",
            "budget": 500,
            "timeline_days": 45,
            "service": "workflow automation",
            "message": ""
        })
        self.assertEqual(d.tier, "WARM")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            score_lead({
                "name": "C",
                "email": "invalid",
                "budget": 100,
                "timeline_days": 60,
                "service": "automation"
            })

if __name__ == "__main__":
    unittest.main()
