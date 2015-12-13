from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext as _

from cooking.tests import util


__author__ = 'sarace'


class TestRecipeView(TestCase):
    def setUp(self):
        """
        Prepare the tests :
         - Create user and set permission
        :return:
        """
        util.initTestUser()


    def test_index_with_no_latest_recipes(self):
        """
        Test the recipes_index view when no recipe are found in latest_recipes (no recipe in database)
        :return:
        """

        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('cooking:recipes_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_recipes'], [])

    def test_index_with_latest_recipes(self):
        """
        Test the recipes_index view when a recipe is found in latest_recipes (>=1 recipe in database)
        :return:
        """

        util.create_test_recipe()
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('cooking:recipes_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_recipes'], ['<Recipe: Tarte Tatin>'])

    def test_search_without_result(self):
        with self.assertRaises(KeyError) :
            """
            Test the search engine , with no results
            context['recipe'] raise a NoKeyError
            """
            util.create_test_recipe()
            self.client.login(username='test_user', password='test_password')
            response = self.client.post(reverse('cooking:recipe_search'),{'recipe_search' : 'Crumble'})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context['recipes'])

    def test_search_with_result(self):
        with self.assertRaises(KeyError) :
            """
            Test the search engine with results
            context['info_message'] raise a KeyError
            :return:
            """

            util.create_test_recipe()
            self.client.login(username='test_user', password='test_password')
            response = self.client.post(reverse('cooking:recipe_search'),{'recipe_search' : 'Tatin'})
            self.assertEqual(response.status_code, 200)
            self.assertQuerysetEqual(response.context['recipes'], ['<Recipe: Tarte Tatin>'])
            self.assertTrue(response.context['latest_recipes'])
            self.assertFalse(response.context['info_messages'])