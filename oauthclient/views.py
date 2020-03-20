import json
import requests
import random
import string
from urllib import parse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse

STATE = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def create_login_url():
    redirect_url = reverse('response')
    redirect_url = parse.quote(f'http://localhost:8000/{redirect_url}')
    url = f'{settings.API_HOST}{settings.OAUTH_TOKEN_ENDPOINT}?'
    url = f'{url}response_type={settings.GRANT_TYPE}&'
    url = f'{url}client_id={settings.CLIENT_ID}&'
    url = f'{url}redirect_url={redirect_url}&'
    url = f'{url}scope={settings.SCOPE}&'
    url = f'{url}state={STATE}'
    return url

def index(request):
    context = {
        'target_url': create_login_url()
    }
    print(context)
    return render(request, 'oauthclient/index.html', context)

def oauth_response(request):
    token = request.GET.get('code', '')
    state = request.GET.get('state', '')
    params = {
        'org_id': '1',
        #'csrfmiddlewaretoken': csrf_token,
    }
    headers = {
        'content-type':'application/json',
        'Authorization': f'Bearer {token}',
    }
    r = requests.get(settings.API_HOST + settings.API_ENDPOINT,
                     headers=headers,
                     data=json.dumps(params))
    context = {
        'token': token,
        'payload': r.text,
        'api_url': f'{settings.API_HOST}{settings.API_ENDPOINT}',
    }
    response = render(request, 'oauthclient/detail.html', context) 
    return response
