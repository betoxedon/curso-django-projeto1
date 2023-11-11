from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class CategoryViewTest(RecipeTestBase):

    # CATEGORY  #
    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'This is a category test'
        self.make_recipe(title=title)

        response = self.client.get(reverse('recipes:category', args=(1, )))
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn(title, content)
        self.assertEqual(len(recipes), 1)

    def test_recipe_detail_template_loads_correct_recipe(self):
        title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(title, content)

    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        """
            Test if recipe is_published False don't show in template
        """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', 
                                           kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)

