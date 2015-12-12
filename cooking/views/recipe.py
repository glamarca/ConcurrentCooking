"""
The recipe controller
"""
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from cooking.models.IngredientRecipe import IngredientRecipe, Ingredient
from cooking.models.Recipe import Recipe
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils import timezone
from cooking.references.Enums import INGREDIENT_TYPES, MEASUREMENT

__author__ = 'sarace'


@login_required(login_url='/authentication/sign_in/')
def recipes_index(request):
    """
     Manage index of recipes pages
     :param request: the http request
     :return: The index view with a context
     """
    latest_recipes = Recipe.objects.order_by('-created')[:10]
    context = {'latest_recipes': latest_recipes, }
    return render(request, 'recipes.html', context)


@login_required(login_url='/authentication/sign_in/')
def details(request, recipe_id):
    """
    Manage the detail page of a recipe
    :param request: the http request
    :param recipe_id : the id of the recipe we want to display details
    :return:The details view of the specified recipe
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients_recipe = IngredientRecipe.objects.filter(recipe=recipe)
    context = {
        'recipe': recipe,
        'ingredients_recipe': ingredients_recipe,
    }
    return render(request, 'recipe.html', context)


@login_required(login_url='/authentication/sign_in/')
def search(request):
    """
    Search a recipe corresponding to 'recipe_search' in POST
    :param request: the http request
    :return: The recipes view with the result of the research
    """
    if request.POST['recipe_search']:
        recipes = Recipe.objects.filter(Q(name__icontains=request.POST['recipe_search']) |
                                        Q(description__icontains=request.POST['recipe_search'])).order_by('-name')
    else :
        recipes = Recipe.objects.all().order_by('-name')
    context = {
        'latest_recipes': Recipe.objects.order_by('-created')[:10],
    }
    if not recipes:
        info_message = _('No results')
        context['info_messages'] = (info_message,)
    else:
        context['recipes'] = recipes
    return render(request, 'recipes.html', context)


@login_required(login_url='/authentication/sign_in/')
@user_passes_test(lambda u: u.has_perm('cooking.change_recipe') or u.has_perm('cooking.add_recipe'))
def recipe_form(request, recipe_id):
    """
    Manage the recipe form
    :param request: the httprequest
    :param recipe_id: The id of the recipe (None if it is a new recipe)
    :return:The forms with the recipe fields if it is an update
    """
    recipe = None
    action = 'add'
    ingredients = []
    if recipe_id:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        action = 'modify'
        ingredients = IngredientRecipe.objects.filter(recipe=recipe)
    context = {
        'recipe': recipe,
        'action': action,
        'ingredients': ingredients,
        'all_ingredients': Ingredient.objects.all().order_by('-name'),
        'all_measurements': dict((key, _(value)) for (key, value) in MEASUREMENT),
    }
    return render(request, 'recipe_form.html', context)


@login_required(login_url='/authentication/sign_in/')
@permission_required('cooking.delete_recipe')
def delete(request, recipe_id):
    """
    Delete a recipe
    :param request: the http request
    :param recipe_id: the id of the recipe we want to delete
    :return:The recipe view
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    context = {
        'latest_recipes': Recipe.objects.order_by('-created')[:10],
        'succes_messages': (_('Recipe deleted'),),
    }
    return render(request, 'recipes.html', context)


@login_required(login_url='/authentication/sign_in/')
@user_passes_test(lambda u: u.has_perm('cooking.change_recipe') or u.has_perm('cooking.add_recipe'))
def add_modify(request):
    """
    Perform the update/creation of a recipe with informations in POST
    :param request: the http request
    :return:the recipe view filled with the created/updated recipe
    """
    recipe = Recipe()
    if ('add' == request.POST['action'] and request.user.has_perm('cooking.add_recipe')) or (
                    'modify' == request.POST['action'] and request.user.has_perm('cooking.change_recipe')):
        if 'add' == request.POST['action']:
            recipe.created = timezone.now()
        else:
            recipe = get_object_or_404(Recipe, pk=request.POST['id'])
        recipe.name = request.POST['name']
        recipe.costs = int(request.POST['cost'])
        recipe.difficulty = int(request.POST['difficulty'])
        recipe.num_people = int(request.POST['num_people'])
        recipe.description = request.POST['description']
        if request.POST['global_time']:
            recipe.global_time = int(request.POST['global_time'])
        recipe.modified = timezone.now()
        if request.POST['preparation_time']:
            recipe.preparation_time = int(request.POST['preparation_time'])
        if request.POST['waiting_time']:
            recipe.waiting_time = int(request.POST['waiting_time'])
        recipe.process = request.POST['process']
        recipe.user_mod = request.user.username
        recipe.save()
        ingredients_recipes = IngredientRecipe.objects.filter(recipe=recipe)
        context = {
            'recipe': recipe,
            'ingredients_recipes': ingredients_recipes,
        }
        return render(request, 'recipe.html', context)
    else:
        context = {
            'latest_recipes': Recipe.objects.order_by('-created')[:10],
            'error_messages': (_('Insufisant privileges'),),
        }
        return render(request, 'recipes.html', context)


@login_required(login_url='/authentication/sign_in/')
@permission_required('cooking.change_recipe')
def add_ingredient_to_recipe(request):
    """
    Add an ingredient to a recipe
    :param request: the http request
    :return: The recipe view updated
    """
    ingredient = get_object_or_404(Ingredient, pk=request.POST['ingredient_id'])
    ir = IngredientRecipe()
    ir.ingredient = ingredient
    if request.POST['recipe_id']:
        recipe = get_object_or_404(Recipe, pk=request.POST['recipe_id'])
    else:
        recipe = Recipe()
    ir.recipe = recipe
    ir.quantity = float(request.POST['quantity'])
    ir.measurement = request.POST['measurement']
    ir.save()
    context = {
        'recipe': recipe,
        'action': request.POST['action'],
        'ingredients': IngredientRecipe.objects.filter(recipe=recipe),
        'all_ingredients': Ingredient.objects.all().order_by('-name'),
        'all_measurements': dict((key, _(value)) for (key, value) in MEASUREMENT),
    }
    return render(request, 'recipe_form.html', context)


@login_required(login_url='/authentication/sign_in/')
@permission_required('cooking.change_recipe')
def delete_ingredient_recipe(request, ingredient_recipe_id, action):
    """
    Remove an ingredient from a recipe
    :param request: the http request
    :param ingredient_recipe_id: the id of the inredient_recipe relational object
    :param action: 'add' or 'modify'
    :return:The recipe view updated
    """
    ingredient_recipe = get_object_or_404(IngredientRecipe, pk=ingredient_recipe_id)
    recipe = ingredient_recipe.recipe
    ingredient_recipe.delete()
    context = {
        'recipe': recipe,
        'action': action,
        'ingredients': IngredientRecipe.objects.filter(recipe=recipe),
        'all_ingredients': Ingredient.objects.all().order_by('-name'),
        'all_measurements': dict((key, _(value)) for (key, value) in MEASUREMENT),
    }
    return render(request, 'recipe_form.html', context)
