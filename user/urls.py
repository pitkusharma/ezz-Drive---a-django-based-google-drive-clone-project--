from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = "user"
urlpatterns = [
    path("", login_user, name = "login" ),
    path("login/", login_user, name = "login" ),
    path("signup/", sign_up, name = "sign-up" ),
    path("logout/", logout_user, name = "logout" ),
    path("edit/", edit_user, name = "edit" ),
    path("details/", details, name = "details" ),
    path("password-change/", password_change, name = "password-change" ),
]