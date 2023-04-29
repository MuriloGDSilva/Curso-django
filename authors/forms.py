from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password']

        labels = {
            'username': ' Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': ' E-mail',
            'password': 'Password',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty'
            },

            'password': {
                'required': 'This field must not be empty'
            }
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': ' Type your username here'
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Type your E-mail here'
            }),

            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your First name here'
            }),

            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your Last name here'
            }),
        }
