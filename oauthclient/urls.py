from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('oauth/token', views.oauth_response, name='response'),
    re_path(r'(?P<path>.*)', views.proxy_view),
]
