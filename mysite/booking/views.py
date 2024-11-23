from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.db.utils import IntegrityError
from .forms import SearchTravelForm, PurchaseTicketForm
from .models import Travel, Ticket, Customer, CITIES

def travel(request):
    context = {
        "cities": CITIES,
    }
    return render(request,"booking/travel.html",context)

def select_ticket(request):
    context = {"cities": CITIES,"request":request.POST}
    form = SearchTravelForm(request.POST)
    if form.is_valid():
        date = form.cleaned_data["date"]
        origin = form.cleaned_data["origin"]
        destination = form.cleaned_data["destination"]
        travels = Travel.objects.filter(schedule__date=date).filter(
            origin=origin,
            destination=destination,
        )
        travel_times = [travel.schedule.strftime("%H:%M") for travel in travels]
        context.update({"travel_times":travel_times})
    else:
        context.update({"dict":form.errors.as_data()})
            
    if request.POST["action"] == "Buy":
        form2 = PurchaseTicketForm(request.POST)
        if form2.is_valid():
            time = form2.cleaned_data["time"]
            origin = form2.cleaned_data["origin"]
            destination = form2.cleaned_data["destination"]
            travel = Travel.objects.get(
                schedule__time=time,
                origin=origin,
                destination=destination,
            )
            # Customer and price are test
            ticket = Ticket(
                customer = Customer.objects.get(pk=3),
                travel = travel,
                seat_number = form2.cleaned_data["seat"],
                price = 1000,
            )
            try:
                ticket.save()
            except IntegrityError:
                context.update({"dict":"The seat you chose is already sold, please select another"})
            else:
                return HttpResponseRedirect(reverse("booking:confirm"))
        else:
            context.update({"dict2":form2.errors.as_data()})

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