"""
The ingredient controller
"""
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from cooking.models.Ingredient import Ingredient
from cooking.models.IngredientRecipe import IngredientRecipe
from django.utils.translation import ugettext as _
from cooking.references.Enums import INGREDIENT_TYPES

__author__ = 'sarace'


@login_required(login_url='/authentication/sign_in/')
def ingredients_index(request):
    """
    Manage index of ingredients pages
    :param request: the http request
    :return: The index view with a context
    """
    latest_ingredients = Ingredient.objects.order_by('-created')[:10]
    context = {'latest_ingredients': latest_ingredients, }
    return render(request, 'ingredients.html', context)


@login_required(login_url='/authentication/sign_in/')
def details(request, ingredient_id):
    """
    Manage the detail page of a recipe
    :param request: the http request
    :param ingredient_id: the id of the ingredient we want to display details
    :return:The details view of the specified ingredient
    """
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    recipes = set(IngredientRecipe.objects.filter(ingredient=ingredient).order_by('-recipe__name'))
    context = {
        'ingredient': ingredient,
        'recipes': recipes,
    }
    return render(request, 'ingredient.html', context)


@login_required(login_url='/authentication/sign_in/')
def search(request):
    """
    Search a ingredient corresponding to 'ingredient_search' in POST
    :param request: the http request
    :return: The ingredients view with the result of the research
    """
    if(request.POST['ingredient_search']):
        ingredients = Ingredient.objects.filter(name__icontains=request.POST['ingredient_search']).order_by('-name')
    else:
        ingredients = Ingredient.objects.all().order_by('-name')
    context = {
        'latest_ingredients': Ingredient.objects.order_by('-created')[:10],
    }
    if not ingredients:
        info_message = _('No results')
        context['info_messages'] = (info_message,)
    else:
        context['ingredients'] = ingredients
    return render(request, 'ingredients.html', context)


@login_required(login_url='/authentication/sign_in/')
@user_passes_test(lambda u: u.has_perm('cooking.change_ingredient') or u.has_perm('cooking.add_ingredient'))
def ingredient_form(request, ingredient_id):
    """
    Manage the ingredient form
    :param request: the httprequest
    :param ingredient_id: The id of the ingredients (None if it is a new ingredient)
    :return:The forms with the ingredient fields if it is an update
    """
    ingredient = None
    action = 'add'
    if ingredient_id :
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        action = 'modify'
    context = {
        'ingredient': ingredient,
        'action': action,
        'ingredient_types' : dict((key,_(value)) for (key,value) in INGREDIENT_TYPES),
    }
    return render(request, 'ingredient_form.html', context)


@login_required(login_url='/authentication/sign_in/')
@permission_required('cooking.delete_ingredient')
def delete(request, ingredient_id):
    """
    Delete an ingredient
    :param request: the http request
    :param ingredient_id: the id of the ingredient we want to delete
    :return:The ingredients view
    """

    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    ingredient.delete()
    context = {
        'latest_ingredients': Ingredient.objects.order_by('-created')[:10],
        'succes_messages': (_('Ingredient deleted'),),
    }
    return render(request, 'ingredients.html', context)


@login_required(login_url='/authentication/sign_in/')
@user_passes_test(lambda u: u.has_perm('cooking.change_ingredient') or u.has_perm('cooking.add_ingredient'))
def add_modify(request):
    """
    Perform the update/creation of an ingredient with information in POST
    :param request: the http request
    :return:the ingredient view filled with the created/updated ingredient
    """
    ingredient = Ingredient()
    if ('add' == request.POST['action'] and request.user.has_perm('cooking.add_ingredient')) or (
                    'modify' == request.POST['action'] and request.user.has_perm('cooking.change_ingredient')):
        if 'add' == request.POST['action']:
            ingredient.created = timezone.now()
        else:
            ingredient = get_object_or_404(Ingredient, pk=request.POST['id'])
        ingredient.name = request.POST['name']
        ingredient.type = request.POST['type']
        ingredient.modified = timezone.now()
        ingredient.user_mod = request.user.username
        ingredient.save()
        recipes = set(IngredientRecipe.objects.filter(ingredient=ingredient).order_by('-recipe__name'))
        context = {
            'ingredient': ingredient,
            'recipes': recipes,
        }
        return render(request, 'ingredient.html', context)
    else:
        context = {
            'latest_ingredients': Ingredient.objects.order_by('-created')[:10],
            'error_messages': (_('Insufficient privileges'),),
        }
    return render(request, 'ingredients.html', context)
