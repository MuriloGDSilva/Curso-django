
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_view_category_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returs_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category',
                                           kwargs={'category_id': 1}))
        response_content = response.content.decode('utf-8')
        self.assertIn(needed_title, response_content)

    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id':
                                                recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_category_paginated_correct(self):
        category_test = self.make_category()
        for r in range(18):
            kwargs = {'slug': f's-{r}',
                      'author_data': {'username': f'u{r}'},
                      'title': 'TestTitle'}
            self.make_recipe_same_with_category(
                category_data=category_test, **kwargs)

        response = self.client.get(reverse('recipes:category', kwargs={
                                   'category_id': 1}))

        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 9)
        self.assertEqual(len(paginator.get_page(2)), 9)
