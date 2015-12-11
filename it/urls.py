__author__ = 'sarace'

from django.conf.urls import url
from .views import it

app_name="it"

urlpatterns = [
    url(r'^$',it.index,name='it_index'),
]
