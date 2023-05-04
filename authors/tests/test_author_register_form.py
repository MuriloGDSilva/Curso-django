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
        [('email', 'The e-mail must be valid.')]
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
