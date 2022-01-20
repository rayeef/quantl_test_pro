from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from . import views
from .views import index
from .polygon_api_client import polygon_crypto_data

app_name = 'MVP'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'frame/', TemplateView.as_view(template_name="MVP/frame.html"), name='frame'),
  	path('demo/', views.demo, name= 'demo'),
    path('backtester/', views.backtester, name='backtester'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('preferences/', views.preferences, name='preferences'),
    path('security/', views.security, name='security'),
    path('linkedaccounts/', views.linkedaccounts, name='linkedaccounts'),
    path('trader/', views.trader, name='trader'),
    path('apiaccess/', views.apiaccess, name='apiaccess'),
    path('billing/', views.billing, name='billing'),
    path('limits/', views.limits, name='limits'),
    path('editplan/', views.editplan, name='editplan'),
    path("register/", views.register_request, name="register"),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name= 'logout'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('password_reset',views.password_reset_request, name='password_reset'),
    # path('stock_screener/',views.stock_screener,name='stock_screener'),
    path('fetch_ig_account',views.fetch_ig_account,name='fetch_ig_account'),
    path('fetch_crypto_data', polygon_crypto_data, name="fetch_crypto_data"),
]
