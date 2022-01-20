from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from .bitoasis_api import *

app_name = 'bitoasis'

urlpatterns = [
    path('connect_broker', connect_bitoasis, name='connect_broker')
]
