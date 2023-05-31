
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsLogOutTest(TestCase):

    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='Tester_user',
                                 password='P@sswordtester')

        self.client.login(username='Tester_user',
                          password='P@sswordtester')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn('Invalid logout request',
                      response.content.decode('utf-8'))

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='Tester_user',
                                 password='P@sswordtester')

        self.client.login(username='Tester_user',
                          password='P@sswordtester')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'Another_user'},
            follow=True,

        )

        self.assertIn('Invalid logout user',
                      response.content.decode('utf-8'))

    def test_user_can_logout_successefully(self):
        User.objects.create_user(username='Tester_user',
                                 password='P@sswordtester')

        self.client.login(username='Tester_user',
                          password='P@sswordtester')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'Tester_user'
            },
            follow=True,

        )

        self.assertIn('user logged out successfully',
                      response.content.decode('utf-8'))
