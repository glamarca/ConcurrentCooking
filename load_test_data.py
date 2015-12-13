#!/usr/bin/env python3

from functools import reduce
import os

DATA_FIXTURES = [
        '001_ingredient_test_data.json',
        '002_recipe_test_data.json',
        '003_ingredient_recipe_test_data.json',
]

ARGS = reduce(lambda s1,s2 : s1 + ' ' + s2,DATA_FIXTURES)
COMMAND = 'python manage.py loaddata '+ARGS
print(COMMAND)
os.system(COMMAND)
