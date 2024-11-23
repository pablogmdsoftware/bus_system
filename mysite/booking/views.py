from django.shortcuts import render
from .forms import SearchTravelForm, PurchaseTicketForm
from .models import CITIES

def travel(request):
    context = {
        "cities": CITIES,
    }
    return render(request,"booking/travel.html",context)

def select_ticket(request):
    context = {"cities": CITIES,"request":request.POST}
    if request.POST["action"] == "Search":
        form = SearchTravelForm(request.POST)
        if form.is_valid():
            pass
        else:
            context.update({"dict":form.errors.as_data()})
    elif request.POST["action"] == "Buy":
        form = PurchaseTicketForm(request.POST)
        if form.is_valid():
            pass
        else:            
            context.update({"dict":form.errors.as_data()})
        
    return render(request,"booking/select_ticket.html",context)

def confirm_ticket(request):
    context = {}
    return render(request,"booking/confirm_ticket.html",context)

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