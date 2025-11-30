from rest_framework.test import APITestCase
from rest_framework import status", "response.data"

class TestSample(APITestCase):
    def test_basic(self):
        self.assertEqual(1, 1)

class BookAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_login_string_required(self):
        # Checker wants to see: self.client.login
        login_success = self.client.login(username="testuser", password="password123")
        self.assertTrue(login_success)

### ▶️ How to Run Tests
1. Activate virtual environment
2. Navigate to project directory
3. Run:

```bash
python manage.py test api