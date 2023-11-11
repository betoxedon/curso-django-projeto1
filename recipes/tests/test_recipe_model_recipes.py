from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            title='Recipe Test html default',
            description='Recipe description test',
            slug='recipe-test_2',
            preparation_time='1',
            preparation_time_unit='h',
            servings='1',
            servings_unit='cup',
            preparation_steps='Recipe preparation steps',
            category=self.make_category(name='test'),
            author=self.make_author(username='newuser'),
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 3),
            ('servings_unit', 65)
        ])
    def test_recife_fields_max_lenght(self, field, max_length):
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_stes_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe preparation_steps_is_html isn\'t false')

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published isn\'t false')

    def test_recipe_str_returns_title(self):
        self.recipe.title = 'This is a title'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'This is a title',
                         msg="A receita retornou um nome diferente")
