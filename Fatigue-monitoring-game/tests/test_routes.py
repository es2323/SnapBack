import unittest
from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_redirects(self):
        res = self.app.get('/dashboard', follow_redirects=True)
        self.assertIn(b"SnapBack", res.data)

    def test_login_page_loads(self):
        res = self.app.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome Back", res.data)

    def test_fake_login_fails(self):
        res = self.app.post('/login', data=dict(email="fake@email.com", password="wrong"), follow_redirects=True)
        self.assertIn(b"Invalid email or password", res.data)
    
    def test_submit_score_api(self):
        response = self.app.post('/submit_score', json={
            "user_email": "test@example.com",
            "game_type": "reaction",
            "reaction_time": 500,
            "fatigue_score": 50,
            "accuracy": 95,
            "errors": 2,
            "completion_time": 3.1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Score submitted successfully", response.data)


if __name__ == "__main__":
    unittest.main()
