import unittest
from src.api_gateway.authentication import login, generate_token
from src.api_gateway.session_management import create_session, terminate_session
from src.api_gateway.validation import validate_input

class TestAPIGateway(unittest.TestCase):

    def test_login_success(self):
        response = login("test_user", "test_password")
        self.assertTrue(response['success'])
        self.assertIn('token', response)

    def test_login_failure(self):
        response = login("wrong_user", "wrong_password")
        self.assertFalse(response['success'])
        self.assertNotIn('token', response)

    def test_generate_token(self):
        token = generate_token("test_user")
        self.assertIsNotNone(token)

    def test_create_session(self):
        session_id = create_session("test_user")
        self.assertIsNotNone(session_id)

    def test_terminate_session(self):
        session_id = create_session("test_user")
        result = terminate_session(session_id)
        self.assertTrue(result)

    def test_validate_input_success(self):
        valid_data = {"query": "What is the status of my order?"}
        self.assertTrue(validate_input(valid_data))

    def test_validate_input_failure(self):
        invalid_data = {"query": ""}
        self.assertFalse(validate_input(invalid_data))

if __name__ == '__main__':
    unittest.main()