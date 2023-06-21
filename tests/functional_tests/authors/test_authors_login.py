
from django.urls import reverse
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsLoginTestForm(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        str_password = 'Pass'
        user = User.objects.create_user(
            username='UserTester', password=str_password)

        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        user_name_filed = self.get_by_placeholder(form, 'Type your username')
        user_name_filed.send_keys(user.username)

        password_field = self.get_by_placeholder(form, 'Type your password')
        password_field.send_keys(str_password)

        form.submit()

        self.assertIn(f'Your are logged in.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

        self.sleep(10)

    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn('Not Found', self.browser.find_element(
            By.TAG_NAME, 'body').text)
        self.sleep(7)

    def test_login_error_user_do_not_exist(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_valid = 'Tester'
        password_valid = '@12339Tester'

        user_name_filed = self.get_by_placeholder(form, 'Type your username')
        user_name_filed.send_keys(username_valid)

        password_field = self.get_by_placeholder(form, 'Type your password')
        password_field.send_keys(password_valid)

        form.submit()

        self.assertIn('User do not exist', self.browser.find_element(
            By.TAG_NAME, 'body').text)

        self.sleep(10)

    def test_login_error_invalid_credentials(self):

        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_invalid = ' ' * 10
        password_invalid = ' ' * 10

        user_name_filed = self.get_by_placeholder(form, 'Type your username')
        user_name_filed.send_keys(username_invalid)

        password_field = self.get_by_placeholder(form, 'Type your password')
        password_field.send_keys(password_invalid)

        form.submit()

        self.assertIn('Invalid credentials.', self.browser.find_element(
            By.TAG_NAME, 'body').text)

        self.sleep(10)



