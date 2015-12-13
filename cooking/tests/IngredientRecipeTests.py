from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone
from cooking.models.Ingredient import Ingredient
from cooking.models.IngredientRecipe import IngredientRecipe
from cooking.models.Recipe import Recipe
from cooking.tests import util

__author__ = 'sarace'


class IngredientRecipeMethodsTests(TestCase):

    def test_create_ingredient_recipe(self):
        """
        Create an ingredientrecipe and test if the relations with recipe and ingredient is correct
        :return:
        """
        recipe, ingredient = util.create_recipe_and_ingredient()
        ingredient_recipe = IngredientRecipe()
        ingredient_recipe.recipe = recipe
        ingredient_recipe.ingredient = ingredient
        ingredient_recipe.quantity=500
        ingredient_recipe.measurement='GR'
        ingredient_recipe.save()
        self.assertTrue(ingredient_recipe.recipe.id == recipe.id)
        self.assertTrue(ingredient_recipe.ingredient.id == ingredient.id)


    def test_update_ingredient_recipe(self):
        """
        Create another ingredient , change the ingredient from a recipe with the new one , test the relations
        :return:
        """
        now = timezone.now()
        recipe, ingredient = util.create_recipe_and_ingredient()
        ingredient_recipe = IngredientRecipe()
        ingredient_recipe.recipe = recipe
        ingredient_recipe.ingredient = ingredient
        ingredient_recipe.quantity=500
        ingredient_recipe.measurement='GR'
        ingredient_recipe.save()
        self.assertTrue(ingredient_recipe.ingredient.id == ingredient.id)
        ingredient_2 = Ingredient(name='Pomme', type='FT', created=now, modified=now, user_mod="cooking_user_test")
        ingredient_2.save()
        self.assertTrue(ingredient_2.id is not None)
        ingredient_recipe.ingredient = ingredient_2
        ingredient_recipe.save()
        self.assertFalse(ingredient_recipe.ingredient.id == ingredient.id)
        self.assertTrue(ingredient_recipe.ingredient.id == ingredient_2.id)

    def test_delete_ingredient_recipe(self):
        with self.assertRaises(ObjectDoesNotExist):
            """
            delete the relation between recipe and ingredient , and test the deletion
            :return:
            """
            recipe, ingredient = util.create_recipe_and_ingredient()
            ingredient_recipe = IngredientRecipe()
            ingredient_recipe.recipe = recipe
            ingredient_recipe.ingredient = ingredient
            ingredient_recipe.quantity=500
            ingredient_recipe.measurement='GR'
            ingredient_recipe.save()
            self.assertTrue(ingredient_recipe.ingredient.id == ingredient.id and
                            ingredient_recipe.recipe.id == recipe.id)
            ingredient_from_rel = IngredientRecipe.objects.get(ingredient = ingredient).ingredient
            recipe_from_db = IngredientRecipe.objects.get(recipe=recipe).recipe
            self.assertTrue(ingredient_from_rel.id is not None and
                            recipe_from_db.id is not None)
            ingredient_recipe.delete()
            IngredientRecipe.objects.get(recipe=recipe_from_db)
            IngredientRecipe.objects.get(ingredient=ingredient_from_rel)