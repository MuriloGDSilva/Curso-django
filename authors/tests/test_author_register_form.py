from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormTest(TestCase):
    @parameterized.expand(
        [('username', 'Type your username here'),
         ('email', 'Type your E-mail here'),
         ('first_name', 'Type your First name here'),
         ('last_name', 'Type your Last name here'),
         ('password', 'Type your password'),
         ('password2', 'Repeat your password')]
    )
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand(
        [('email', 'The e-mail must be valid.'),
         ('username', 'Username must have letters, numbers or one of those @.+-_'
          'The lenght should between 4 and 150 characters.')]
    )
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(help_text, current_help_text)

    @parameterized.expand(
        [('username', 'Username'),
         ('email', 'E-mail'),
         ('first_name', 'First Name'),
         ('last_name', 'Last Name'),
         ('password', 'Password'),
         ('password2', 'Password')]
    )
    def test_fields_labels_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(label, current_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
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

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'This field must not be empty'),
        ('last_name', 'This field must not be empty'),
        ('email', 'This field must not be empty'),
        ('password', 'This field must not be empty'),
        ('password2', 'This field must not be empty'),

    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_lenght_should_be_4(self):
        self.form_data['username'] = 'lyo'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Your username must be at least 4 characters long'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_lenght_should_be_150(self):
        self.form_data['username'] = 'a'*152
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Your username can be a maximum of 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letter_and_numbers(self):
        self.form_data['password'] = '144as'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password must have at last one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.')
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_equal(self):
        # confimation error
        self.form_data['password'] = '@A1249mu'
        self.form_data['password2'] = '@A1249mur'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'You entered different passwords'

        self.assertIn(msg, response.content.decode('utf-8'))

        # comfirmation equal
        self.form_data['password'] = '@A1249mu'
        self.form_data['password2'] = '@A1249mu'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'You entered different passwords'

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_if_form_in_the_method_get_returns_404(self):
        self.form_data
        url = reverse('authors:create')
        response = self.client.get(url, self.form_data)
        self.assertEqual(response.status_code, 404)
