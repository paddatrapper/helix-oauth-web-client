import base64
import json
import requests
import random
import string
from urllib import parse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from proxy.views import proxy_view as django_proxy

STATE = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def create_code_login_url():
    url = f'{settings.API_HOST}'
    redirect_url = reverse('response')
    redirect_url = parse.quote(f'http://localhost:8000/{redirect_url}')
    url = f'{url}{settings.OAUTH_TOKEN_AUTHORIZE_ENDPOINT}?'
    url = f'{url}response_type=code&'
    url = f'{url}client_id={settings.CLIENT_ID}&'
    url = f'{url}redirect_url={redirect_url}&'
    url = f'{url}scope={settings.SCOPE}&'
    url = f'{url}state={STATE}'
    return url

def index(request):
    context = {
        'code_target_url': create_code_login_url(),
        'client_target_url': reverse('response'),
    }
    return render(request, 'oauthclient/index.html', context)

def oauth_response(request):
    token = request.GET.get('code', '')
    state = request.GET.get('state', '')
    context = {
        'token': token,
        'api_url': f'{settings.API_HOST}{settings.API_ENDPOINT}',
        'api_endpoint': settings.API_ENDPOINT,
    }
    response = render(request, 'oauthclient/detail.html', context)
    return response

def generate_authorization():
    credential = f'{settings.CC_CLIENT_ID}:{settings.CC_CLIENT_SECRET}'
    encoded_credential = base64.b64encode(credential.encode('utf-8')).decode()
    return encoded_credential

def get_csrf():
    response = requests.get(settings.API_HOST)
    print(response.cookies)
    return response.cookies.get('csrftoken')

def proxy_view(request, path):
    csrf = get_csrf()
    remote_url = f'{settings.API_HOST}/{path}'
    authorization = generate_authorization()
    extra_requests_args = {
        'headers': {
            'Authorization': f'Basic {authorization }',
        },
        'cookies': {
            'csrftoken': csrf,
        },
    }
    return django_proxy(request, remote_url, extra_requests_args)
