
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=testsearch')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(
            reverse('recipes:search') + '?q=TestSearchTerm')
        self.assertIn('Search for &quot;TestSearchTerm&quot;',
                      response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(slug='one', author_data={
                                   'username': 'one'}, title=title1)
        recipe2 = self.make_recipe(slug='two', author_data={
                                   'username': 'two'}, title=title2)

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=This')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])