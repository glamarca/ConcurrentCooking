#!/usr/bin/env python

from functools import reduce
import os


TESTS_CLASSES = [
    'cooking.tests.IngredientTests',
    'cooking.tests.RecipeTests',
    'cooking.tests.IngredientRecipeTests',
    'cooking.tests.TestRecipeView',
]

ARGS = reduce(lambda s1,s2 : s1+' '+s2, TESTS_CLASSES)
COMMAND = 'python manage.py test -v 2 '+ARGS
os.system(COMMAND)
