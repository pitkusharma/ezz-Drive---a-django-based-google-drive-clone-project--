from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import *
from .models import *


def home(request, *args, **kwargs):

    if request.method == "GET":
        context = {}
        context["folder_form"] = FolderForm()
        context["file_form"] = FileForm()
        context["folder"] = kwargs["folder"]
        return render(request, "drive/home.html", context)


def file_upload(request, *args, **kwargs):

    if request.method == "POST":
        folder = Folder.objects.get(id = kwargs["folder"])
        date_time = datetime.now()
        file = request.FILES.getlist("file_upload")
        for i in file:
            try:
                new_entry = File(
                file = i, 
                name = i.name,
                size = i.size,
                date_of_upload = date_time,
                folder = folder
                )
                new_entry.save()
            except:
                continue


        return HttpResponseRedirect(reverse(
            "drive:home", 
            kwargs={
                'folder': folder.id
                } ))


def create_folder(request, *args, **kwargs):

    if request.method == "POST":
        form = FolderForm(request.POST)
        parent_folder = kwargs["folder"]

        if form.is_valid():
            user = request.user
            name = form.cleaned_data.get("name")

            new_entry = Folder(
                user = user,
                parent_folder = parent_folder,
                name = name
            )
            new_entry.save()

        return HttpResponseRedirect(reverse(
        "drive:home", 
        kwargs={
            'folder': parent_folder
            } ))