from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url_home = reverse('recipes:home')
        self.assertEqual(url_home, '/')

    def test_recipe_category_url_is_correct(self):
        category_url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(category_url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        recipe_detail_url = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(recipe_detail_url, '/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        url_search = reverse('recipes:search')
        self.assertEqual(url_search, '/recipes/search/')
