from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from .binance.rest import BinanceRest

app_name = 'binance'

urlpatterns = [
    path('connect_broker', BinanceRest.connect_binance, name='connect_broker')
]
