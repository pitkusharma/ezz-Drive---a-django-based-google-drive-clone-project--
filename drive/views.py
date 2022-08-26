from django.shortcuts import render


def home(request):

    context = {}

    return render(request, "drive/home.html", context)

# Create your views here.
