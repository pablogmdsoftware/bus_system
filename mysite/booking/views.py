from django.shortcuts import render
from .forms import SearchTravel
from .models import CITIES

def travel(request):
    context = {
        "form": SearchTravel,
        "cities": CITIES.values(),
    }
    return render(request,"booking/travel.html",context)

def mytickets(request):
    context = {}
    return render(request,"booking/mytickets.html",context)

def mypasses(request):
    context = {}
    return render(request,"booking/mypasses.html",context)

def about(request):
    context = {}
    return render(request,"booking/about.html",context)

def profile(request):
    context = {}
    return render(request,"booking/profile.html",context)

def singin(request):
    context = {}
    return render(request,"booking/singin.html",context)