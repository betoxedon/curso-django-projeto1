from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class SearchViewTest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_raises_200_if_search_term(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertEqual(response.status_code, 200)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<teste>')
        self.assertIn('Pesquisar por &quot;&lt;teste&gt;&quot;', response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'},
            description='Testing search recipes'
        )
        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'},
            description='Another test recipe'
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        description_response1 = self.client.get(f'{search_url}?q=testing')
        description_response2 = self.client.get(f'{search_url}?q=another')
        description_both = self.client.get(f'{search_url}?q=recipe')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

        self.assertIn(recipe1, description_response1.context['recipes'])
        self.assertNotIn(recipe2, description_response1.context['recipes'])

        self.assertIn(recipe2, description_response2.context['recipes'])
        self.assertNotIn(recipe1, description_response2.context['recipes'])

        self.assertIn(recipe1, description_both.context['recipes'])
        self.assertIn(recipe2, description_both.context['recipes'])