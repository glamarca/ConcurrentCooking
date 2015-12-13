from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from cooking.models.Ingredient import Ingredient
from cooking.models.Recipe import Recipe

__author__ = 'sarace'

def initTestUser():
    """

    :return:
    """
    user = User.objects.create_user('test_user', 'test@testing.org', 'test_password')
    content_type = ContentType.objects.get_for_model(Recipe)
    ch_recipe_perm = Permission.objects.get(content_type=content_type, codename='change_recipe')
    add_recipe_perm = Permission.objects.get(content_type=content_type, codename='add_recipe')
    del_recipe_perm = Permission.objects.get(content_type=content_type, codename='delete_recipe')
    user.user_permissions.add(ch_recipe_perm,add_recipe_perm,del_recipe_perm)
    user.save()

def create_test_ingredient():
    """

    :return:
    """
    now = timezone.now()
    ingredient = Ingredient(name='Mandarine', type='FT', created=now, modified=now, user_mod="cooking_user_test")
    ingredient.save()
    return ingredient

def create_test_recipe():
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

def create_recipe_and_ingredient():
    """
    Inityialise and save a recipe and an ingredient
    :return:(recipe,ingredient)
    """
    recipe = create_test_recipe()
    ingredient = create_test_ingredient()
    return recipe,ingredient