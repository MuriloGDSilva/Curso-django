from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsregisterTest(AuthorsBaseTest):

    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Strongp@ssword',
            'password2': 'Strongp@ssword',
        }
        return super().setUp(*args, **kwargs)

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*15)

    def test_empty_fields_error_messages(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@gmail.com')
        button_enter = form.find_element(By.TAG_NAME, 'button')
        button_enter.click()

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.assertIn('This field must not be empty', form.text)
        self.sleep(15)

    def test_field_password_with_passwords_many_different(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@gmail.com')

        password_field = self.get_by_placeholder(form, 'Type your password')
        password_field.send_keys('@12339Xe')

        password_field_2 = self.get_by_placeholder(
            form, 'Repeat your password')
        password_field_2.send_keys('@12339Xer')

        password_field_2.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.assertIn('You entered different passwords', form.text)
        self.sleep(20)

    def test_field_password_out_of_standard(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@gmail.com')

        password_field = self.get_by_placeholder(form, 'Type your password')
        password_field.send_keys('thetest')

        password_field_2 = self.get_by_placeholder(
            form, 'Repeat your password')
        password_field_2.send_keys('thetest')

        password_field_2.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        error_message = (
            'Password must have at last one uppercase '
            'letter, one lowercase letter and one number. The '
            'lenght should be at least 8 characters.'
        )

        self.assertIn(error_message, form.text)
        self.sleep(20)

    def test_register_created_with_sucsess(self):

        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        first_name = self.get_by_placeholder(form, 'Type your First name here')
        first_name.send_keys('first')

        last_name = self.get_by_placeholder(form, 'Type your Last name here')
        last_name.send_keys('last')

        user_name = self.get_by_placeholder(form, 'Type your username here')
        user_name.send_keys('user')

        email = self.get_by_placeholder(form, 'Type your E-mail here')
        email.send_keys('email@anyemail.com')

        password = self.get_by_placeholder(form, 'Type your password')
        password.send_keys('Strongp@ssword1685')

        password_2 = self.get_by_placeholder(form, 'Repeat your password')
        password_2.send_keys('Strongp@ssword1685')
        password_2.send_keys(Keys.ENTER)

        body_form_login = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Your user is created, please log in.',
                      body_form_login.text)

        self.sleep(10)
