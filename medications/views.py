import requests
from django.shortcuts import render
from django.http import HttpResponse

from authentication.views import refresh_token, get_token
from .models import RefillTracker


BASE_URL = 'https://drchrono.com/'

# Create your views here.
def list_medications(request):
    current_user = request.user
    if request.GET.get('code', None):
        refresh_token(request, request.GET['code'], current_user)

    access_token = get_token(request, current_user)
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    medications = requests.get(BASE_URL + 'api/medications', headers=headers).json()
    context = {
        'medications_list': medications['results'],
        'next': medications['next'],
        'previous': medications['previous']
    }
    return render(request, 'medications/index.html', context)

def refill_medication(request):
    prescription = request.body
