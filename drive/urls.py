from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = "drive"
urlpatterns = [
    path("", home, name = "home" ),
]