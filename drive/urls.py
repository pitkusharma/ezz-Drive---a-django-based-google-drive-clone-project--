from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = "drive"
urlpatterns = [
    path("<int:folder>/", home, name = "home" ),
    path("file-upload/<int:folder>/", file_upload, name = "file-upload"),

    path("create-folder/<int:folder>/", create_folder, name = "create-folder")
]