from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = "user"
urlpatterns = [
    path("signup/", sign_up, name = "sign-up" ),
    path("login/", login_user, name = "login" ),
]