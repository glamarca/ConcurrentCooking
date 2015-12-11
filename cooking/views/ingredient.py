from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from cooking.models.Ingredient import Ingredient
from cooking.models.IngredientRecipe import IngredientRecipe

__author__ = 'sarace'

@login_required(login_url='/authentication/sign_in/')
def ingredients_index(request):
    latest_ingredients = Ingredient.objects.order_by('-created')[:10]
    context = { 'latest_ingredients' : latest_ingredients,}
    return render(request,'ingredients.html',context)

@login_required(login_url='/authentication/sign_in/')
def details(request,ingredient_id):
    ingredient = get_object_or_404(Ingredient,pk=ingredient_id)
    recipes = set(IngredientRecipe.objects.filter(ingredient=ingredient).order_by('-name'))
    context = {
        'ingredient' : ingredient,
        'recipes' : recipes,
        }
    return render(request,'ingredient.html',context)