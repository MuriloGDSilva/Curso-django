from django import forms
from recipes.models import Recipe
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


class DashboardCreateRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover')

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),

            'preparation_time_unit': forms.Select(
                choices=(
                    ('minutos', 'Minutos'),
                    ('horas', 'Horas'),
                )
            ),

            'servings_unit': forms.Select(
                choices=(
                    ('porçoes', 'Porções'),
                    ('fatias', 'Fatias'),
                    ('pessoas', 'Pessoas'),

                )
            )

        }

        error_messages = {
            'title': {
                'required': 'This field must not be empty'
            },

            'description': {
                'required': 'This field must not be empty'
            },

            'preparation_time': {
                'required': 'This field must not be empty'
            },

            'servings': {
                'required': 'This field must not be empty'
            },

            'preparation_steps': {
                'required': 'This field must not be empty'
            },
        }

    def clean(self):

        super_clean = super().clean()

        cleaned_data_field = self.cleaned_data
        title_field = cleaned_data_field.get('title')
        description_field = cleaned_data_field.get('description')

        if title_field == description_field:
            self._my_errors['title'].append(
                'The title cannot match the description'
            )
            self._my_errors['description'].append(
                'The description cannot match the title'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):

        cleaned_title = self.cleaned_data.get('title', '')

        if len(cleaned_title) < 5 or len(cleaned_title) > 20:
            self._my_errors['title'].append(
                'The title must be between 5 to 20 characters.')
        return cleaned_title

    def clean_description(self):

        cleaned_description = self.cleaned_data.get('description', '')

        if len(cleaned_description) < 10 or len(cleaned_description) > 30:
            self._my_errors['description'].append(
                'The description must be between 10 to 30 characters.'
            )
        return cleaned_description

    def clean_preparation_time(self):

        cleaned_preparation_time = self.cleaned_data.get(
            'preparation_time', '')

        if not is_positive_number(cleaned_preparation_time):
            self._my_errors['preparation_time'].append(
                'enter only whole numbers'
            )

        return cleaned_preparation_time

    def clean_servings(self):

        cleaned_servings = self.cleaned_data.get('servings', '')

        if not is_positive_number(cleaned_servings):
            self._my_errors['servings'].append(
                'enter only whole numbers'
            )

        return cleaned_servings

    def clean_preparation_steps(self):
        cleaned_preparation_steps = self.cleaned_data.get(
            'preparation_steps', '')

        if len(cleaned_preparation_steps) < 50:
            self._my_errors['preparation_steps'].append(
                'Preparation steps must be at least 50 characters long.'
            )

        return cleaned_preparation_steps
