from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = "drive"
urlpatterns = [
    path("", home, name = "home-default" ),

    path("<int:folder>/", home, name = "home" ),
    path("create-folder/<int:folder>/", create_folder, name = "create-folder"),
    path("delete-folder/<int:id>/", delete_folder, name = "delete-folder"),
    path("rename-folder/<int:id>/", rename_folder, name = "rename-folder"),

    path("file-upload/<int:folder>/", file_upload, name = "file-upload"),
    path("rename-file/<int:id>/", rename_file, name = "rename-file"),
    path("download-file/<int:id>/", download_file, name = "download-file"),
    path("delete-file/<int:id>/", delete_file, name = "delete-file"),
]