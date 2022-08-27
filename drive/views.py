from django.shortcuts import render

from .forms import *


def home(request):

    if request.method == "GET":
        context = {}
        context["folder_form"] = FolderForm()
        context["file_form"] = FileForm()
        return render(request, "drive/home.html", context)



# Create your views here.
