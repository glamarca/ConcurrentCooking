from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import get_template
from cooking.models.Ingredient import Ingredient
from cooking.models.Recipe import Recipe

__author__ = 'sarace'

@login_required(login_url='/authentication/sign_in/')
def index(request):
    return render(request,'index.html')

