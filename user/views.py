from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def sign_up(request):
    
    if request.method == "GET":
        context = {}
        form = UserProfileForm()
        context["form"] = form
        return render(request, "user/signup.html", context)

    elif request.method == "POST":
        context = {}
        form = UserProfileForm(request.POST)
        context["form"] = form
        
        if form.is_valid():

            new_user = User.objects.create_user(username = form.cleaned_data["email"], 
                first_name = form.cleaned_data["first_name"],last_name = form.cleaned_data["last_name"], 
                email = form.cleaned_data["email"], password = form.cleaned_data["password"]
            )
            user_profile = UserProfile(user = new_user, gender = form.cleaned_data["gender"])
            user_profile.save()
            
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
            
            return HttpResponseRedirect(reverse("drive:home", 
            kwargs={
                "folder": 1
            })) 

        return render(request, "user/login.html", context)



