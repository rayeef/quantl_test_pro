from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from .auth_main import *

app_name = 'coinbase'

urlpatterns = [
    path('connect_broker', Coinbase.connect_coinbase, name='connect_broker')
]
