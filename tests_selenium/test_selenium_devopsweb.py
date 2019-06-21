from flask import url_for
from flask_testing import LiveServerTestCase
from bcrypt import gensalt, hashpw

from config import config_dict
from app import create_app, db
from app.models import User

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import logging
import time
import unittest


"""Don't show logging messages while testing."""
logging.disable(logging.CRITICAL)


class TestBase(LiveServerTestCase):
    """A base test case."""

    def create_app(self):
        app = create_app(config_dict['Test1'])
        app.config.update(
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=8933
        )
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(
            options=options,
            executable_path="./tests_selenium/geckodriver",
            log_path="./tests_selenium/geckodriver.log")
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
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
        self.driver.quit()


class TestRegistrationAndLoginCase(TestBase):

    def test_selenium_registration_and_login(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly and that user will be
        redirected to the login page.
        Then test that a user can login and that they will be redirected to
        the homepage.
        """

        """Click register menu link."""
        self.driver.find_element_by_id("register").click()
        time.sleep(1)

        """Fill in registration form."""
        self.driver.find_element_by_id("username").send_keys(
            "testuser1")
        self.driver.find_element_by_id("email").send_keys(
            "testuser1@test.com")
        self.driver.find_element_by_id("password").send_keys(
            "123")
        self.driver.find_element_by_id("confirm_password").send_keys(
            "123")
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        """Assert that browser redirects to login page."""
        assert url_for('users_blueprint.login') in self.driver.current_url

        """Assert success message is shown."""
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "Your account has been created!" in success_message

        """Fill in login form."""
        self.driver.find_element_by_id("email").send_keys("testuser1@test.com")
        self.driver.find_element_by_id("password").send_keys("123")
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        """Assert that browser redirects to home page."""
        element = self.driver.find_element_by_tag_name('h3')
        assert element.text == 'Home'


class TestPages(TestBase):

    def test_selenium_home_page(self):
        """Ensure that the home page works correctly."""
        page_link = self.get_server_url() + url_for('home_blueprint.home')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads home page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'Home'

    def test_selenium_overview_flask_page(self):
        """Ensure that the overview flask page works correctly."""
        page_link = self.get_server_url() + url_for(
            'overview_flask_blueprint.overview_flask')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads overview flask page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'Flask Overview'

    def test_selenium_overview_docker_page(self):
        """Ensure that the overview docker page works correctly."""
        page_link = self.get_server_url() + url_for(
            'overview_docker_blueprint.overview_docker')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads overview docker page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'Docker Overview'

    def test_selenium_overview_kubernetes_page(self):
        """Ensure that the overview kubernetes page works correctly."""
        page_link = self.get_server_url() + url_for(
            'overview_kubernetes_blueprint.overview_kubernetes')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads overview kubernetes page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'Kubernetes Overview'

    def test_selenium_overview_sqlite_page(self):
        """Ensure that the overview sqlite page works correctly."""
        page_link = self.get_server_url() + url_for(
            'overview_sqlite_blueprint.overview_sqlite')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads overview sqlite page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'SQLite Commands and General Usage'

    def test_selenium_overview_postgresql_page(self):
        """Ensure that the overview postgresql page works correctly."""
        page_link = self.get_server_url() + url_for(
            'overview_postgresql_blueprint.overview_postgresql')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads overview postgresql page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'PostgreSQL Overview'

    def test_selenium_overview_ansible_page(self):
        """Ensure that the overview ansible page works correctly."""
        page_link = self.get_server_url() + url_for(
            'overview_ansible_blueprint.overview_ansible')
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads overview ansible page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'Ansible Overview'

    def test_selenium_page_not_found_error(self):
        """Ensure that custom not found page works correctly."""
        page_link = self.get_server_url() + '/nopage'
        self.driver.get(page_link)
        time.sleep(1)

        """Assert that browser loads not found page."""
        element = self.driver.find_element_by_id('devopsweb-page-title')
        assert element.text == 'Page Not Found.'


if __name__ == '__main__':
    unittest.main()
