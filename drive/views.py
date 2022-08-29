from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

@login_required
def home(request, *args, **kwargs):

    if request.method == "GET":
        context = {}
        context["folder_form"] = FolderForm()
        context["file_form"] = FileForm()
        
        try:
            folder = Folder.objects.get(id = kwargs["folder"])
            context["folder"] = folder.id
            if folder.user != request.user:
                return HttpResponseRedirect(reverse("drive:home-default"))    
        except:
            folder = Folder.objects.get(user = request.user, parent_folder = None)
            return HttpResponseRedirect(reverse("drive:home",
            kwargs = {
                "folder": folder.id
            }))

        folder_stack = []
        folder_stack.append(folder)

        temp = folder
        while temp.parent_folder != None:
            temp = Folder.objects.get(id = temp.parent_folder)
            folder_stack.append(temp)
        
        context["folder_stack"] = folder_stack[::-1]

        folder_list = Folder.objects.filter(parent_folder = folder.id).order_by("id")
        context["folder_list"] = folder_list
        
        if (not "order" in request.session  
        and not "reverse" in request.session):
            request.session["order"] = "date"
            request.session["reverse"] = False
        
        if request.session["order"] == "date":
            if request.session["reverse"] == True:
                files = File.objects.filter(folder = folder).order_by("date_of_upload")
            else:
                files = File.objects.filter(folder = folder).order_by("-date_of_upload")
        
        elif request.session["order"] == "name":
            if request.session["reverse"] == True:
                files = File.objects.filter(folder = folder).order_by("-name")
            else:
                files = File.objects.filter(folder = folder).order_by("name")
        
        elif request.session["order"] == "size":
            if request.session["reverse"] == True:
                files = File.objects.filter(folder = folder).order_by("-size")
            else:
                files = File.objects.filter(folder = folder).order_by("size")

        else:
            files = File.objects.filter(folder = folder).order_by("-date_of_upload")

        context["files"] = files

        param_dict = {
            "order": request.session["order"],
            "reverse": request.session["reverse"]
        }
        params_form = SetParameterForm(initial = param_dict)
        context["params_form"] = params_form

        context["rename_form"] = RenameForm()

        return render(request, "drive/home.html", context)

    elif request.method == "POST":
        form = SetParameterForm(request.POST)
        if form.is_valid():
            request.session["order"] = form.cleaned_data["order"]
            request.session["reverse"] = form.cleaned_data["reverse"]

        return HttpResponseRedirect(reverse("drive:home", kwargs={
            "folder": kwargs["folder"]
        }))

@login_required
def file_upload(request, *args, **kwargs):

    if request.method == "POST":
        folder = Folder.objects.get(id = kwargs["folder"])
        
        if folder.user != request.user:
            return HttpResponseRedirect(reverse("drive:home-default"))

        date_time = datetime.now()
        file = request.FILES.getlist("file_upload")
        for i in file:
            new_entry = File(
            file = i, 
            name = i.name,
            size = i.size,
            date_of_upload = date_time,
            folder = folder
            )
            new_entry.save()
            
        return HttpResponseRedirect(reverse(
            "drive:home", 
            kwargs={
                'folder': folder.id
                } ))

@login_required
def create_folder(request, *args, **kwargs):

    if request.method == "POST":
        form = FolderForm(request.POST)

        if form.is_valid():
            folder = Folder.objects.get(id = form.cleaned_data["folder"])

            if folder.user != request.user:
                return HttpResponseRedirect(reverse("drive:home-default"))

            user = request.user
            name = form.cleaned_data.get("name")

            new_entry = Folder(
                user = user,
                parent_folder = folder.id,
                name = name
            )
            new_entry.save()

        return HttpResponseRedirect(reverse(
        "drive:home", 
        kwargs={
            'folder': folder.id
            } ))

@login_required
def rename_file(request, *args, **kwargs):
    file = File.objects.get(id = kwargs["id"])

    if request.user != file.folder.user:
        return HttpResponseRedirect(reverse("drive:home-default"))
    
    if request.method == "POST":
        form = RenameForm(request.POST)
        if form.is_valid():
            temp = ""
            for i in file.name[::-1]:
                if i != ".":
                    temp = i + temp
                else:
                    temp = i + temp
                    break
            file.name = form.cleaned_data["name"] + temp
            file.save()
        
        return HttpResponseRedirect(reverse("drive:home", kwargs={
            "folder": file.folder.id
        }))

@login_required
def delete_file(request, *args, **kwargs):
    file = File.objects.get(id = kwargs["id"])

    if request.user != file.folder.user:
        return HttpResponseRedirect(reverse("drive:home-default"))

    if request.method == "GET":
        folder = file.folder.id
        file.delete()
        return HttpResponseRedirect(reverse("drive:home", kwargs={
            "folder": folder
        }))

@login_required
def rename_folder(request, *args, **kwargs):
    folder = Folder.objects.get(id = kwargs["id"])
    
    if request.user != folder.user:
        return HttpResponseRedirect(reverse("drive:home-default"))
    
    if request.method == "POST":
        form = RenameForm(request.POST)
        if form.is_valid():
            
            folder.name = form.cleaned_data["name"] 
            folder.save()
        
        return HttpResponseRedirect(reverse("drive:home", kwargs={
            "folder": folder.parent_folder
        }))

@login_required
def delete_folder(request, *args, **kwargs):
    folder = Folder.objects.get(id = kwargs["id"])
 
    if request.user != folder.user:
        return HttpResponseRedirect(reverse("drive:home-default"))
    
    if request.method == "GET":
        parent_folder = folder.parent_folder
        folder.delete()
 
        return HttpResponseRedirect(reverse("drive:home", kwargs={
            "folder": parent_folder
        }))

        

