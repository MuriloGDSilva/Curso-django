from django.test import TestCase
from recipes.models import Recipe, Category, User


class RecipeMixin:

    def make_recipe_bacth(self, qtd):
        recipes = []
        for r in range(qtd):
            kwargs = {
                'title': f'Title-Recipe-Test{r}',
                'slug': f's-{r}',
                'author_data': {'username': f'u{r}'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes

    def make_category(self, name='categoria'):
        return Category.objects.create(name='name')

    def make_author(self,
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='123456',
                    email='username@gmail.com',
                    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(self,
                    category_data=None,
                    author_data=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='Recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit='Porçoes',
                    preparation_steps='Recipe preparation steps',
                    preparation_steps_is_html=False,
                    is_published=True,
                    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_same_with_category(self,
                                       category_data,
                                       author_data=None,
                                       title='Recipe Title',
                                       description='Recipe Description',
                                       slug='Recipe-slug',
                                       preparation_time=10,
                                       preparation_time_unit='Minutos',
                                       servings=5,
                                       servings_unit='Porçoes',
                                       preparation_steps='Recipe preparation steps',
                                       preparation_steps_is_html=False,
                                       is_published=True,
                                       ):

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=category_data,
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
