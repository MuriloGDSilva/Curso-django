from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .test_recipe_base import RecipeBaseFunctionalTest
from unittest.mock import patch
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Not Found Recipes', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_bacth(qtd=10)
        title_need = recipes[0].title = 'This is what i need'
        recipes[0].save()
       
        self.browser.get(self.live_server_url)   
       
        search_input = self.browser.find_element(By.CLASS_NAME, "search-input")
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(title_need, self.browser.find_element
                      (By.CLASS_NAME, "main-content-list").text)
        self.sleep(2)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_pagination(self):
        self.make_recipe_bacth(10)

        self.browser.get(self.live_server_url)
        pagination = self.browser.find_element(
            By.XPATH, 
            '//a[@aria-label="Go to page 2"]'
        )
        pagination.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)

        self.sleep(10)


