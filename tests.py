import unittest

from server import app
from model import db, connect_to_db, test_data


class ServerTests(unittest.TestCase):
    """Tests for my PetShare site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test index page loads correctly."""

        result = self.client.get("/")
        self.assertIn("Find your furry BFF", result.data)


class ServerTestsDatabase(unittest.TestCase):
    """Flask tests that uses petshare database."""

    def setUp(self):
        """Set up env for every test before testing db."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        test_data()

    def tearDown(self):
        """Clean env after every test."""

        db.session.close()
        db.drop_all()

    def test_user_profile(self):
        """Test User profile loads successfully."""

        result = self.client.get('/user/1')
        self.assertEquals(200, result.status_code)
        self.assertIn("Charlie Brown", result.data)

    def test_pet_profile(self):
        """Test pet profile loads successfully."""

        result = self.client.get('/pet_profile/1')
        self.assertEquals(200, result.status_code)
        self.assertIn("Snoopy", result.data)


if __name__ == "__main__":
    unittest.main()
