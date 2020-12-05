from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('oauth/token', views.oauth_response, name='response'),
    path('oauth/authorization-code', views.oauth_get_authorization, name='oauth_get_authorization'),
]
