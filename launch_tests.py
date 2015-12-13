#!/usr/bin/env python

from functools import reduce
import os,sys,getopt

# Tests Classes
#==============

# Unit tests classes
UNIT_TESTS_CLASSES = [
    'cooking.tests.IngredientTests',
    'cooking.tests.RecipeTests',
    'cooking.tests.IngredientRecipeTests',
    'cooking.tests.TestRecipeView',
]

# Selenium tests classes
SELENIUM_TESTS_CLASSES = [
    'cooking.tests.SeleniumHealtTest'
]

# All tests classes
ALL_TESTS_CLASSES = UNIT_TESTS_CLASSES + SELENIUM_TESTS_CLASSES
COMMAND = 'python manage.py test -v 2 '+ARGS

def main(argv):
    try:
        opts,args = getopt.getopt(argv,"hat:",["--help","type="])
    except getopt.GetoptError:
        print 'Usage : launch_test.py <OPTIONS> [ARGS]]'
        print 'Type launch_test.py -h to see options'
        sys.exit(2)
    for opt,arg int opts :
        if opt=='-h':
            print('launch_test.py <OPTIONS> [ARGS]')
            print('OPTIONS : ')
            print(' -h : Show this message')
            print(' -t <TYPE> : Launch the tests of a specific type')
            print('     TYPE :')
            print('      selenium : Selenium tests')
            print('      unit : Unit tests tests')
            print(' -a : Run testst of all types')
            sys.exit()
        elif opt == "-t" :
            if arg is None :
                print 'Usage : launch_test.py <OPTIONS> [ARGS]'
                print 'Type launch_test.py -h to see options'
                sys.exit(2)
            elif arg == "unit" :
                ARGS = reduce(lambda s1,s2 : s1+' '+s2, UNIT_TESTS_CLASSES)
            elif arg == "selenium" :
                ARGS = reduce(lambda s1,s2 : s1+' '+s2, UNIT_TESTS_CLASSES)
        elif opt == "-a" :
            ARGS = reduce(lambda s1,s2 : s1+' '+s2, ALL_TESTS_CLASSES)

    os.system(COMMAND)

if __name__ == "__main__" :
    main(sys.argv[1:])
