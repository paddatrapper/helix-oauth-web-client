import base64
import json
import requests
import random
import string
from urllib import parse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse

STATE = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

GRANT_TYPE_CODE = 'code'
GRANT_TYPE_CLIENT = 'client_credentials'

def create_login_url(grant_type):
    url = f'{settings.API_HOST}'
    if grant_type == GRANT_TYPE_CODE:
        redirect_url = reverse('response')
        redirect_url = parse.quote(f'http://localhost:8000/{redirect_url}')
        url = f'{url}{settings.OAUTH_TOKEN_AUTHORIZE_ENDPOINT}?'
        url = f'{url}response_type={grant_type}&'
        url = f'{url}client_id={settings.CLIENT_ID}&'
        url = f'{url}redirect_url={redirect_url}&'
        url = f'{url}scope={settings.SCOPE}&'
        url = f'{url}state={STATE}'
    elif grant_type == GRANT_TYPE_CLIENT:
        url = f'{url}{settings.OAUTH_TOKEN_ENDPOINT}'
    return url

def index(request):
    context = {
        'code_target_url': create_login_url(GRANT_TYPE_CODE),
        'client_target_url': create_login_url(GRANT_TYPE_CLIENT),
        'client_redirect_url': reverse('response')
    }
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

def oauth_get_authorization(request):
    credential = f'{settings.CC_CLIENT_ID}:{settings.CC_CLIENT_SECRET}'
    encoded_credential = base64.b64encode(credential.encode('utf-8')).decode()
    return JsonResponse({'credential': encoded_credential})
