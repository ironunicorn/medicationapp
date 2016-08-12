import datetime
import os
import pytz
import requests
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import DrChronoAuth

BASE_URL = 'https://drchrono.com/'

def authorize(request):
    return HttpResponseRedirect(BASE_URL + 'o/authorize/?redirect_uri='
                                'http://localhost:8000/medications'
                                '&response_type=code&client_id=' +
                                os.environ['CLIENT_ID'] +
                                '&scope=clinical:read')

def get_token(request, current_user):
    if not request.session.get('access_token', None):
        request.session['access_token'] = current_user.drchronoauth.access_token

    return request.session['access_token']


def refresh_token(request, code, user):
    response = requests.post(BASE_URL + 'o/token/', data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/medications',
        'client_id': os.environ['CLIENT_ID'],
        'client_secret': os.environ['CLIENT_SECRET'],
    })
    response.raise_for_status()
    data = response.json()
    current_user = user
    expires = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
    try:
        dr = current_user.drchronoauth
        dr.access_token = data['access_token']
        dr.refresh_token = data['refresh_token']
        dr.access_token = expires
    except ObjectDoesNotExist:
        dr = DrChronoAuth(
            user=current_user,
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            token_expiration=expires
        )
    dr.save()
    request.session['access_token'] = data['access_token']


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # do stuff
    else:
        pass
        # do other stuff

def logout(request):
    logout(request)
