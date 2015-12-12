from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone
from cooking.models.Recipe import Recipe

__author__ = 'sarace'


class RecipeMethodsTests(TestCase):
    def create_test_recipe(self):
        """
        Initialise a new recipe and save it in the DB
        :return:
        """
        now = timezone.now();
        recipe = Recipe(name='Tarte Tatin', global_time=55, preparation_time=15, difficulty=1, costs=1, num_people=6,
                        created=now, modified=now, user_mod='user_test', description='Tarte aux pommes caramélisées',
                        process='*Peler les pommes et les couper en quartier.\n*Etaler les quartier en cercle dans un moule à tarte....')
        recipe.save()
        return recipe

    def test_create_recipe(self):
        """
        Test the creation of a recipe
        :return:
        """
        self.create_test_recipe()
        new_recipe = Recipe.objects.get(name='Tarte Tatin')
        self.assertTrue(new_recipe.id is not None)
        self.assertTrue(new_recipe.global_time == 55)
        self.assertTrue(new_recipe.preparation_time == 15)
        self.assertTrue(new_recipe.costs == 1)
        self.assertTrue(new_recipe.user_mod == 'user_test')
        self.assertTrue(new_recipe.num_people == 6)

    def test_update_recipe(self):
        """
        Update a recipe, save it and test if the changes were done.
        :return:
        """
        recipe = self.create_test_recipe()
        old_recipe_id = recipe.id
        old_recipe_global_time = recipe.global_time
        recipe.global_time = 60
        recipe.save()
        new_recipe = Recipe.objects.get(name='Tarte Tatin')
        self.assertTrue(old_recipe_id == new_recipe.id)
        self.assertFalse(old_recipe_global_time == new_recipe.global_time)


    def test_delete_recipe(self):
        with self.assertRaises(ObjectDoesNotExist):
            """
            Delete a recipe and check if it is not anymore in the DB
            :return:
            """
            recipe = self.create_test_recipe()
            recipe_id = recipe.id
            recipe.delete()
            deleted_recipe = Recipe.objects.get(pk=recipe_id)
