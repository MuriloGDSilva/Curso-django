
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_funtion_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returs_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page test - it load one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': 1}))
        response_content = response.content.decode('utf-8')
        self.assertIn(needed_title, response_content)

    def test_recipe_detail_template_dont_loads_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)
