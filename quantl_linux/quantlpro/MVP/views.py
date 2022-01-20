from os import stat
from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import json
from django.db import models
from django.core.exceptions import *
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from MVP.models import Graph
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render
from django.contrib.auth.models import User
# User Registration and Login page imports
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout

'''Development specific imports'''
from MVP.polygon_api_client import *
from MVP.ig_api_client import *

import pdb



# no need to change this function. only build the index.html in templates folder
def index(request):
    return render(request, 'MVP/home.html')


def demo(request):
    """object mapping & external functions calling"""

    '''External Functions'''
    # q_volatility, s_volatility, s, q, dia = ploygon_stocks_data()
    # meta, value_spy, max_spy, min_spy, spy_list = polygon_spy_data()
    # value_qqq, max_qqq, min_qqq, qqq_list = polygon_qqq_data()
    # btc, eth, v_btc, v_eth = polygon_crypto_values()
    # value_btc, min_btc, max_btc, btc_list = polygon_btc_data()
    # value_eth, min_eth, max_eth, eth_list = polygon_eth_data()
    # headline_1, headline_2, headline_3, headline_4, headline_5, \
    # ticker_1, ticker_2, ticker_3, ticker_4, ticker_5, utc_1, utc_2, utc_3, utc_4, utc_5, \
    # source_1, source_2, source_3, source_4, source_5 = polygon_news_feed()


    #account_1, account_1_balance, pl1, account_2, account_2_balance, pl2, \
    #Name, Size, Direction, Value = ig_fetch_accounts()

    '''End External Function Mapping'''

    # revise this logic
    '''Object Call-outs'''
    # volatility_qqq = q_volatility
    # volatility_spy = s_volatility
    # spy = s
    # qqq = q
    # btc_close = btc
    # eth_close = eth
    # v_btc = v_btc
    # v_eth = v_eth

    return render(request, 'MVP/demo-crypto/dashboards/index.html', context={})
        
        # 'Close_SPY': spy,
                                                                    #          'Close_QQQ': qqq,
                                                                    #          'SPY_DELTA': volatility_spy,
                                                                    #          'QQQ_DELTA': volatility_qqq,
                                                                    #          'BTC_CLOSE': btc_close,
                                                                    #          'ETH_CLOSE': eth_close,
                                                                    #          'VOLATILITY_BTC': v_btc,
                                                                    #          'VOLATILITY_ETH': v_eth,
                                                                    #          'meta': meta,
                                                                    #          'value_spy': value_spy,
                                                                    #          'min_spy': min_spy,
                                                                    #          'max_spy': max_spy,
                                                                    #          'spy_list': spy_list,
                                                                    #          'value_qqq': value_qqq,
                                                                    #          'min_qqq': min_qqq,
                                                                    #          'max_qqq': max_qqq,
                                                                    #          'qqq_list': qqq_list,
                                                                    #          'value_btc': value_btc,
                                                                    #          'max_btc': max_btc,
                                                                    #          'min_btc': min_btc,
                                                                    #          'btc_list': btc_list,
                                                                    #          'value_eth': value_eth,
                                                                    #          'max_eth': max_eth,
                                                                    #          'min_eth': min_eth,
                                                                    #          'eth_list': eth_list,
                                                                    #          'HDG1': headline_1,
                                                                    #          'HDG2': headline_2,
                                                                    #          'HDG3': headline_3,
                                                                    #          'HDG4': headline_4,
                                                                    #          'HDG5': headline_5,
                                                                    #          'TICK1': ticker_1,
                                                                    #          'TICK2': ticker_2,
                                                                    #          'TICK3': ticker_3,
                                                                    #          'TICK4': ticker_4,
                                                                    #          'TICK5': ticker_5,
                                                                    #          'UTC1': utc_1,
                                                                    #          'UTC2': utc_2,
                                                                    #          'UTC3': utc_3,
                                                                    #          'UTC4': utc_4,
                                                                    #          'UTC5': utc_5,
                                                                    #          'URL1': source_1,
                                                                    #          'URL2': source_2,
                                                                    #          'URL3': source_3,
                                                                    #          'URL4': source_4,

                                                                    #          'URL5': source_5
                                                                    # #         'ACC1': account_1,
                                                                    # #         'ACC2': account_2,
                                                                    # #         'BALANCE1': account_1_balance,
                                                                    # #         'BALANCE2': account_2_balance,
                                                                    # #         'PL1': pl1,
                                                                    # #         'PL2': pl2,
                                                                    # #         'POS_NAME': Name,
                                                                    # #         'POS_SIZE': Size,
                                                                    # #         'POS_DIR': Direction,
                                                                    # #         'POS_VALUE': Value

                                                                    #          })


def backtester(request):
    symbol = None
    if request.method == "GET":
        symbol = request.GET.get('stock_symbol')
        print(symbol)
    # Uncomment the line below to debug
    # pdb.set_trace()
    return render(request, 'MVP/demo-crypto/actions/backtester.html', context={'stock_symbol': symbol})


def trader(request):
    return render(request, 'MVP/demo-crypto/dashboards/trader.html')

def myprofile(request):
    return render(request, 'MVP/demo-crypto/settings/myprofile.html')

def limits(request):
    return render(request, 'MVP/demo-crypto/settings/limits.html')

def preferences(request):
    return render(request, 'MVP/demo-crypto/settings/preferences.html')

def security(request):
    return render(request, 'MVP/demo-crypto/settings/security.html')

def linkedaccounts(request):
    return render(request, 'MVP/demo-crypto/settings/linked-accounts.html')

def apiaccess(request):
    return render(request, 'MVP/demo-crypto/settings/api-access.html')

def billing(request):
    return render(request, 'MVP/demo-crypto/dashboards/billing.html')

def editplan(request):
    return render(request, 'MVP/demo-crypto/dashboards/editplan.html')
    

# '''setting up user registration process'''
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("MVP:login")
        messages.error(request, form.errors)
    form = NewUserForm()
    return render(request, 'MVP/register.html', context={"register_form": form})


# '''setting up user login'''


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("MVP:demo")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="MVP/login.html", context={"login_form": form})


# '''Log out functionality'''

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("MVP:home")


# '''Password Reset functionality'''
''' PRODUCTION WARNING
    Update your views.py password_reset_request function
'''


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "MVP/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="MVP/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def fetch_ig_account(request):
    if request.method == "GET":
        print("Fetching IG Accounts")
        account_1, account_1_balance, pl1, account_2, account_2_balance, pl2, \
        Name, Size, Direction, Value = ig_fetch_accounts()
        print(Name, Size, Direction, Value, account_1, account_1_balance, pl1, pl2, account_2, account_2_balance)

        return JsonResponse({"Status":"Successfully fetched account", "data" : {
            "name": Name,
            "account_1": account_1,
            "account_1_balance": account_1_balance,
            "account_2": account_2,
            "account_2_balance": account_2_balance,
            "pl1": pl1,
            "pl2": pl2,
            "Size": json.dumps(Size),
            "Direction": json.dumps(Direction),
            "Value": json.dumps(Value),
        }}, safe=False)
