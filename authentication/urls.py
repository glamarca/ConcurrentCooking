from .views import authentication


__author__ = 'sarace'

from django.conf.urls import url


app_name="authentication"

urlpatterns = [
    url(r'^sign_in/$',authentication.sign_in,name="sign_in"),
    url(r'^do_sign_in/$',authentication.do_sign_in,name='do_sign_in'),
    url(r'^logout/$',authentication.log_out,name='logout'),
]
