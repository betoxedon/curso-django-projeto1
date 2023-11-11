from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            "No recipes found here",
            response.content.decode('utf-8')
            )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        content = response.content.decode('utf-8')
        recipe = Recipe.objects.get(pk=1)
        self.assertIn(recipe.title, content)
        self.assertIn(f"{recipe.preparation_time}" +
                      f" {recipe.preparation_time_unit}", content)
        self.assertIn(f"{recipe.servings}" +
                      f" {recipe.servings_unit}", content)
        self.assertIn(recipe.category.name, content)
        self.assertIn(f"{recipe.author.first_name}" +
                      f" {recipe.author.last_name}", content)
        self.assertEqual(len(recipes), 1)

    def test_recipe_home_template_dont_loads_recipes(self):
        """
            Test if recipe is_published False don't show in template
        """
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            "No recipes found here",
            response.content.decode('utf-8')
            )
