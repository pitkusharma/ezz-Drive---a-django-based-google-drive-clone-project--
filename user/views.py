# from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from drive.models import Folder

from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def sign_up(request):
    
    if request.method == "GET":
        context = {}
        form = SignupForm()
        context["form"] = form
        return render(request, "user/signup.html", context)

    elif request.method == "POST":
        context = {}
        form = SignupForm(request.POST)
        context["form"] = form
        
        if form.is_valid():

            new_user = User.objects.create_user(
                username = form.cleaned_data["email"], 
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"], 
                email = form.cleaned_data["email"], 
                password = form.cleaned_data["password"]
            )

            user_profile = UserProfile(user = new_user, gender = form.cleaned_data["gender"])
            user_profile.save()

            home_folder = Folder(
                user = new_user,
                name = "home",
                parent_folder = None,
            )
            home_folder.save()
            folders = ["Videos", "Images", "Docs"]
            for i in folders:
                temp = Folder(
                    user = new_user,
                    name = i,
                    parent_folder = home_folder.id,
                    )
                temp.save()

            return HttpResponseRedirect(reverse("user:login"))
        
        return render(request, "user/signup.html", context)
        
def login_user(request):

    if request.method == "GET":
        context = {}
        form = LoginForm()
        context["form"] = form
        return render(request, "user/login.html", context)

    elif request.method == "POST":
        context = {}
        form = LoginForm(request.POST)
        context["form"] = form
        
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data.get("user_name"),
                password = form.cleaned_data.get("password")
            )
            login(request, user)
            
            return HttpResponseRedirect(reverse("drive:home-default")) 

        return render(request, "user/login.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("user:login"))


def edit_user(request, *args, **kwargs):
    
    if request.method == "GET":
        form_user = UserForm(
            instance = request.user,
            prefix = "user"
            )
        form_user_profile = UserProfileForm(
            instance = request.user.userprofile,
            prefix = "user_profile"
            )

        context = {}
        context["form1"] = form_user
        context["form2"] = form_user_profile

        return render(request, "user/edit.html", context)

    elif request.method == "POST":
        form_user = UserForm(request.POST, instance = request.user, prefix ="user")
        form_user_profile = UserProfileForm(request.POST, instance = request.user.userprofile, 
        prefix ="user_profile")

        if form_user.is_valid() and form_user_profile.is_valid():
            form_user.save()
            form_user_profile.save()
    
        context = {}
        context["form1"] = form_user
        context["form2"] = form_user_profile

        return render(request, "user/edit.html", context)


def details(request, *args, **kwargs):
    if request.method == "GET":
        context = {}
        context["user"] = request.user

        return render(request, "user/details.html", context)

def password_change(request, *args, **kwargs):
    if request.method == "GET":
        context = {}
        context["form"] = PasswordChange()
        return render(request, "user/password.html", context)

    elif request.method == "POST":
        form = PasswordChange(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data.get("password"))
            request.user.save()

        return HttpResponseRedirect(reverse("user:login"))





