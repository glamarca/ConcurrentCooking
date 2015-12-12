"""
Generic index view for all the modules of concurrent_cooking
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import get_template
from cooking.models.Ingredient import Ingredient
from cooking.models.Recipe import Recipe

__author__ = 'sarace'

@login_required(login_url='/authentication/sign_in/')
def index(request):
    """
    Manage index view
    :param request: the http request
    :return:the index view
    """
    return render(request,'index.html')

