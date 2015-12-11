from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

__author__ = 'sarace'

def sign_in(request):
    return render(request,'sign_in.html',)

def do_sign_in(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('index'))
            else:
                # Return a 'disabled account' error message
                return render(request,'sign_in.html',{ 'error_messages' : (_('Account Disabled'),),})
        else:
            # Return an 'invalid login' error message.
            return render(request,'sign_in.html',{ 'error_messages' : (_('Invalid user or password'),),})
        return render_to_response('sign_in.html',context_instance=RequestContext(request))
def log_out(request):
    logout(request)
    return render(request,'sign_in.html',{ 'info_messages' : (_('Successfully log out'),),})