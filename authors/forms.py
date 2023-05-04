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
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password'
        }),
        validators=[strong_password],
        label='Password',
        error_messages={
            'required': 'This field must not be empty'
        }
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        label='Password',
        error_messages={
            'required': 'This field must not be empty'
        }
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your First name here',
        }),
        label='First Name',
        error_messages={
            'required': 'This field must not be empty'
        }
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your Last name here',
        }),
        label='Last Name',
        error_messages={
            'required': 'This field must not be empty'
        }
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Type your E-mail here'
        }),
        label='E-mail',
        error_messages={
            'required': 'This field must not be empty'
        },
        help_text='The e-mail must be valid.'
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username here'
        }),
        label='Username',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Your username must be at least 4 characters long',
            'max_length': 'Your username can be a maximum of 150 characters',
        },
        help_text=('Username must have letters, numbers or one of those @.+-_'
                   'The lenght should between 4 and 150 characters.'),
        min_length=4, max_length=150,
    )

    class Meta:

        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'You entered different passwords',
                'password2': 'You entered different passwords'
            })
