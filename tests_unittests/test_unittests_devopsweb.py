from flask_testing import TestCase

from config import config_dict
from app import create_app

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
        pass

    def tearDown(self):
        pass


class TestHomeCase(BaseTestCase):

    """Ensure that root page goes to Home."""
    def test_root_route(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Home', response.data)


class TestErrorPages(BaseTestCase):

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
