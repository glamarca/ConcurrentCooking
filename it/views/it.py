"""
The it controller
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

__author__ = 'sarace'

@login_required(login_url='/authentication/sign_in/')
def index(request):
    """
    Manage the it_index view
    :param request: the http request
    :return:The it_index view
    """
    return render(request,'it_index.html')