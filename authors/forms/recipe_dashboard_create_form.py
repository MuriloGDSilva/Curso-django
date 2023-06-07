from django import forms
from recipes.models import Recipe


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


class DashboardCreateRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

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
