"""
The cooking controller
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cooking.models.Ingredient import Ingredient
from cooking.models.Recipe import Recipe

__author__ = 'sarace'

@login_required(login_url='/authentication/sign_in/')
def index(request):
    """
    Manage index of cooking page
    :param request: the http request
    :return: The cooking_index view with the context
    """
    context = {
        'latest_recipes': Recipe.objects.order_by('-created')[:5],
        'latest_ingredients' : Ingredient.objects.order_by('-created')[:5],
        }
    return render(request,'cooking_index.html',context)