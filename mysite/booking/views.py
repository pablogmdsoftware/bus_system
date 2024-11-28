from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from .forms import SearchTravelForm, PurchaseTicketForm, TicketForm, ProfileForm
from .forms import PasswordForm
from .models import Travel, Ticket, Customer, CITIES

def travel(request):
    context = {
        "cities": CITIES,
        "user": request.user,
    }
    return render(request,"booking/travel.html",context)

@login_required
def select_ticket(request):
    context = {
        "cities": CITIES,
        "request": request.POST,
        "user": request.user,
        "dict": request.user,
    }
    form = SearchTravelForm(request.POST)
    if form.is_valid():
        date = form.cleaned_data["date"]
        origin = form.cleaned_data["origin"]
        destination = form.cleaned_data["destination"]
        travels = Travel.objects.filter(schedule__date=date).filter(
            origin=origin,
            destination=destination,
        )
        # This solution works only for utc+1 timezone servers
        travel_times = []
        for travel in travels:
            travel_times.append((travel.schedule+timedelta(hours=1)).strftime("%H:%M"))
        context.update({"travel_times":travel_times})
    else:
        errors = {key:value[0] for (key,value) in form.errors.items()}
        form_clean_error = errors.get("__all__")
        context.update({"errors":errors,"form_clean_error":form_clean_error})
            
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
            ticket_form = TicketForm({
                "user": User.objects.get(pk=5),
                "travel": travel,
                "seat_number": form2.cleaned_data["seat"],
                "price": 1000,
            })
            if ticket_form.is_valid():
                ticket = Ticket(
                    user = ticket_form.cleaned_data["user"],
                    travel = ticket_form.cleaned_data["travel"],
                    seat_number = ticket_form.cleaned_data["seat_number"],
                    price = ticket_form.cleaned_data["price"],
                )
                ticket.save()
                return HttpResponseRedirect(reverse("booking:confirm"))
            else:
                integrity_error = ticket_form.errors.get("__all__")[0]
                context.update({"integrity_error":integrity_error})                
        else:
            errors2 = {key:value[0] for (key,value) in form2.errors.items()}
            form_clean_error = errors2.get("__all__")
            context.update({"errors2":errors2,"form_clean_error":form_clean_error})

    return render(request,"booking/select_ticket.html",context)

@login_required
def confirm_ticket(request):
    context = {"user": request.user,}
    return render(request,"booking/confirm_ticket.html",context)

@login_required
def mytickets(request):
    context = {"user":request.user,}
    return render(request,"booking/mytickets.html",context)

@login_required
def mypasses(request):
    context = {"user":request.user,}
    return render(request,"booking/mypasses.html",context)

def about(request):
    context = {"user":request.user,}
    return render(request,"booking/about.html",context)

@login_required
def profile(request):
    context = {"user": request.user,"request":request.POST}
    if request.POST.get("action") == "Submit":
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user = User.objects.get(pk=request.user.id)
            customer = Customer.objects.get(user=user)
            new_data = profile_form.cleaned_data

            user.username = new_data["username"]
            user.first_name = new_data["first_name"]
            user.last_name = new_data["last_name"]
            user.email = new_data["email"]
            customer.birth_date = new_data["birth_date"]
            customer.has_large_family = new_data["has_large_family"]
            customer.has_reduced_mobility = new_data["has_reduced_mobility"]

            try:
                user.save()
            except IntegrityError:
                pass
            else:
                customer.save()
                return HttpResponseRedirect(reverse("booking:profile"))
         
        else:
            request.POST["action"] == "Edit information"
            errors = {key:value[0] for (key,value) in profile_form.errors.items()}
            form_clean_error = errors.get("__all__")
            context.update({"errors":errors,"form_clean_error":form_clean_error})
            
    return render(request,"booking/profile.html",context)

def singin(request):
    context = {}
    return render(request,"booking/singin.html",context)

def login_view(request):
    context = {}
    if request.POST.get("action") == "Submit":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("booking:travel"))
        else:
            context.update({"dict":"Error message"})
            return render(request,"booking/login.html",context)
    else:
        return render(request,"booking/login.html",context)

@login_required
def logout_view(request):
    context = {"user":request.user}
    if request.POST.get("action") == "Logout":
        logout(request)
        return HttpResponseRedirect(reverse("booking:travel"))
    else:
        return render(request,"booking/profile.html",context)

@login_required
def change_password(request):
    context = {}
    if request.POST.get("action") == "Submit":
        form = PasswordForm(request.POST)
        user = request.user
        if form.is_valid():
            if user.check_password(form.cleaned_data["old_password"]):
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                return HttpResponseRedirect(reverse("booking:profile"))
            else:
                context.update({"incorrect_password":"Incorrect password"})
                return render(request,"booking/change_password.html",context)
        else:
            context.update({"errors":form.errors})
            context.update({"not_same_password":form.errors.get("__all__")})
            return render(request,"booking/change_password.html",context)
            
    return render(request,"booking/change_password.html")