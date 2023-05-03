from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[1-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at last one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'),

            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        validators=[strong_password],
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        label='Password'
    )

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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'You entered different passwords',
                'password2': 'You entered different passwords'
            })
