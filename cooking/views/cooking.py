from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cooking.models.Ingredient import Ingredient
from cooking.models.Recipe import Recipe

__author__ = 'sarace'

@login_required(login_url='/authentication/sign_in/')
def index(request):
    context = {
        'latest_recipes': Recipe.objects.order_by('-created')[:10],
        'latest_ingredients' : Ingredient.objects.order_by('-created')[:10],
        }
    return render(request,'cooking_index.html',context)