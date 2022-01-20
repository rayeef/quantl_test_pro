from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from .config.trade_ig_config import *

app_name = 'IGServices'

urlpatterns = [
    path('connect_broker', config.connect_broker, name='connect_broker')
]
