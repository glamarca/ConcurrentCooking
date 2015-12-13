from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone
from cooking.models.Ingredient import Ingredient
from cooking.tests import util


class IngredientMethodTests(TestCase):


    def test_create_ingredient(self):
        """
        Create an new Ingredient , save it and check if it is well created.
        :return:
        """
        ingredient = util.create_test_ingredient()
        saved_ingredient = Ingredient.objects.get(name="Mandarine")
        self.assertTrue(saved_ingredient.name == ingredient.name)
        self.assertTrue(saved_ingredient.type == ingredient.type)
        self.assertTrue(saved_ingredient.created == ingredient.created)
        self.assertTrue(saved_ingredient.modified == ingredient.modified)
        self.assertTrue(saved_ingredient.user_mod == ingredient.user_mod)

    def test_update_ingredient(self):
        """
        Create an ingredient , updtate it and check the updates.
        :param selfself:
        :return:
        """
        ingredient = util.create_test_ingredient()
        ingredientID = ingredient.id
        pastName = ingredient.name
        ingredient.name = 'Clementine'
        ingredient.save()
        new_ingredient = Ingredient.objects.get(pk=ingredientID)
        self.assertTrue(new_ingredient.id == ingredientID)
        self.assertFalse(new_ingredient.name == pastName)

    def test_delete_ingredient(self):
        with self.assertRaises(ObjectDoesNotExist):
            """
            Create an ingredient , delete it and test the deletion
            Assert that a ObjectDoesNotExist exception is raised if you get the deleted ingredient
            :return:
            """
            ingredient = util.create_test_ingredient()
            ingredientId = ingredient.id
            ingredient.delete()
            Ingredient.objects.get(pk=ingredientId)


