from flask_login import current_user
from flask_testing import TestCase
from bcrypt import gensalt, hashpw

from config import config_dict
from app import create_app, db
from app.models import User

import logging
import unittest


"""Don't show logging messages while testing."""
logging.disable(logging.CRITICAL)


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app(config_dict['Test2'])
        return app

    def setUp(self):
        db.create_all()

        password = "123"
        hashed_password = hashpw(password.encode('utf8'), gensalt())
        admin = User(username="admin",
                     email="admin@test.com",
                     password=hashed_password)
        testuser1 = User(username="testuser1",
                         email="testuser1@test.com",
                         password=hashed_password)

        testuser2 = User(username="testuser2",
                         email="testuser2@test.com",
                         password=hashed_password)

        db.session.add(admin)
        db.session.add(testuser1)
        db.session.add(testuser2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestLoginLogoutCase(BaseTestCase):

    """Ensure that root page requires user login."""
    def test_root_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Login Form', response.data)

    """Ensure that user goes to home page after login."""
    def test_home_page(self):
        response = self.client.post(
            '/login',
            data=dict(email="admin@test.com", password="123"),
            follow_redirects=True)
        self.assertIn(b'System Configuration', response.data)

    """Ensure that the login page redirects to home after login."""
    def test_login_page_redirects_to_home(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@test.com", password="123"),
                follow_redirects=True)
            response = self.client.get('/login', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home', response.data)
            self.assertTrue(current_user.username == 'admin')

    """Ensure that the login page works correctly with a bad password."""
    def test_login_page_with_bad_password(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@test.com", password="111"),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'403', response.data)
            self.assertIn(b'Forbidden', response.data)

    """Ensure that the logout page works correctly."""
    def test_logout_page(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@test.com", password="123"),
                follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login Form', response.data)


class TestRegistrationCase(BaseTestCase):

    """Ensure that register page works correctly."""
    def test_register_page(self):
        response = self.client.post(
            '/register',
            data=dict(username='testuser3',
                      email="testuser3@test.com",
                      password="123",
                      confirm_password='123'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

    """Ensure that register page works correctly with a taken username."""
    def test_register_page_with_taken_username(self):
        response = self.client.post(
            '/register',
            data=dict(username='testuser1',
                      email="testuser3@test.com",
                      password="123",
                      confirm_password='123'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username is already in use.', response.data)

    """Ensure that register page works correctly with a taken email."""
    def test_register_page_with_taken_email(self):
        response = self.client.post(
            '/register',
            data=dict(username='testuser3',
                      email="testuser2@test.com",
                      password="123",
                      confirm_password='123'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email is already in use.', response.data)

    """Ensure that the register page redirects to home after login."""
    def test_register_page_redirects_to_home(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@test.com", password="123"),
                follow_redirects=True)
            response = self.client.get('/register', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home', response.data)
            self.assertTrue(current_user.username == 'admin')


class TestAccountCase(BaseTestCase):

    """Ensure that the user can get the account page after login."""
    def test_account_page(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@test.com", password="123"),
                follow_redirects=True)
            response = self.client.get('/account')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account Info', response.data)
            self.assertTrue(current_user.username == 'admin')

    """Ensure that the user can update account info."""
    def test_update_account_page(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@test.com", password="123"),
                follow_redirects=True)
            response = self.client.post(
                '/account',
                data=dict(username='admin1',
                          email="admin1@test.com",
                          company="testCompany"),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account Info', response.data)
            self.assertTrue(current_user.username == 'admin1')

    """Ensure that the user can't update account with taken username."""
    def test_update_account_page_with_taken_username(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="testuser1@test.com", password="123"),
                follow_redirects=True)
            response = self.client.post(
                '/account',
                data=dict(username='testuser2',
                          email="testuser1@test.com",
                          company="testCompany"),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account Info', response.data)
            self.assertIn(b'Username already taken.', response.data)
            self.assertTrue(current_user.username == 'testuser1')

    """Ensure that the user can't update account with taken email."""
    def test_update_account_page_with_taken_email(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="testuser1@test.com", password="123"),
                follow_redirects=True)
            response = self.client.post(
                '/account',
                data=dict(username='testuser1',
                          email="testuser2@test.com",
                          company="testCompany"),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account Info', response.data)
            self.assertIn(b'Email already taken.', response.data)
            self.assertTrue(current_user.username == 'testuser1')


class TestResetPasswordCase(BaseTestCase):

    """Ensure that the reset request page works correctly."""
    def test_reset_request_page(self):
        with self.client:
            response = self.client.post(
                '/reset_request',
                data=dict(email="admin@test.com"),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email sent with instructions', response.data)

    """Ensure that the reset request page works correctly with bad account."""
    def test_reset_request_page_with_bad_account(self):
        with self.client:
            response = self.client.post(
                '/reset_request',
                data=dict(email="admin10@test.com"),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account does not exist.', response.data)

    """Ensure that the reset password page works correctly with bad token."""
    def test_reset_password_page_with_bad_token(self):
        with self.client:
            response = self.client.post(
                '/reset_password/123',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'invalid or expired token', response.data)

    """Ensure that the reset token works correctly."""
    def test_reset_token_page_with_valid_token(self):
        with self.client:
            user = User.query.filter_by(email="testuser2@test.com").first()
            token = user.get_reset_token()
            response = self.client.post(
                '/reset_password/' + token,
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Reset Password', response.data)

    """Ensure that resetting password works correctly."""
    def test_resetting_password(self):
        with self.client:
            user = User.query.filter_by(email="testuser2@test.com").first()
            token = user.get_reset_token()
            response = self.client.post(
                '/reset_password/' + token,
                data=dict(password="111",
                          confirm_password='111'),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your password has been updated!', response.data)

    """Ensure that password reset pages work correctly while logged in."""
    def test_password_reset_pages_while_logged_in(self):
        with self.client:
            user = User.query.filter_by(email="testuser2@test.com").first()
            token = user.get_reset_token()
            response = self.client.post(
                '/login',
                data=dict(email="testuser2@test.com", password="123"),
                follow_redirects=True)
            response = self.client.get('/reset_request',
                                       follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home', response.data)
            self.assertTrue(current_user.username == 'testuser2')
            response = self.client.get('/reset_password/' + token,
                                       follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home', response.data)
            self.assertTrue(current_user.username == 'testuser2')


class TestErrorPages(BaseTestCase):

    """Ensure 401 page for unauthorized access works correctly."""
    def test_401_unauthorized_access(self):
        response = self.client.get('/home', follow_redirects=True)
        self.assertIn(b'401', response.data)
        self.assertIn(b'Full authentication is required', response.data)

    """Ensure that the 403 error page works correctly."""
    def test_403_error_page(self):
        response = self.client.get('/devopsweb-403', follow_redirects=True)
        self.assertIn(b'The request has been forbidden', response.data)

    """Ensure that the 404 error page works correctly."""
    def test_404_error_page(self):
        response = self.client.get('/devopsweb-404', follow_redirects=True)
        self.assertIn(b'That page does not exist', response.data)

    """Ensure that the 500 error page works correctly."""
    def test_500_error_page(self):
        response = self.client.get('/devopsweb-500', follow_redirects=True)
        self.assertIn(b'Internal Server Error', response.data)

    """Ensure that the 501 error page works correctly."""
    def test_501_error_page(self):
        response = self.client.get('/devopsweb-501', follow_redirects=True)
        self.assertIn(b'Not Implemented', response.data)

    """Ensure that the 503 error page works correctly."""
    def test_503_error_page(self):
        response = self.client.get('/devopsweb-503', follow_redirects=True)
        self.assertIn(b'Service Unavailable', response.data)


if __name__ == '__main__':
    unittest.main()
