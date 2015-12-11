from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from cooking.models.IngredientRecipe import IngredientRecipe
from cooking.models.Recipe import Recipe
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils import timezone

__author__ = 'sarace'


@login_required(login_url='/authentication/sign_in/')
def recipes_index(request):
    latest_recipes = Recipe.objects.order_by('-created')[:10]
    context = {'latest_recipes': latest_recipes, }
    return render(request, 'recipes.html', context)


@login_required(login_url='/authentication/sign_in/')
def details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients_recipes = IngredientRecipe.objects.filter(recipe=recipe)
    context = {
        'recipe': recipe,
        'ingredients_recipes': ingredients_recipes,
    }
    return render(request, 'recipe.html', context)


@login_required(login_url='/authentication/sign_in/')
def search(request):
    recipes = Recipe.objects.filter(Q(name__icontains=request.POST['recipe_search']) |
                                    Q(description__icontains=request.POST['recipe_search'])).order_by('-name')
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
    recipe = None
    action = 'add'
    if recipe_id:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        action = 'modify'
    return render(request, 'recipe_form.html', {'recipe': recipe, 'action' : action, })


@login_required(login_url='/authentication/sign_in/')
@permission_required('cooking.delete_recipe')
def delete(request, recipe_id):
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
        recipe.global_time = int(request.POST['global_time'])
        recipe.modified = timezone.now()
        recipe.preparation_time = int(request.POST['preparation_time'])
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
