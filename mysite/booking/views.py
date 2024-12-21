from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone
from datetime import date as date_python

from .forms import SearchTravelForm, PurchaseTicketForm, TicketForm, ProfileForm
from .forms import PasswordForm, SingupForm
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
        buses = {}
        for travel in travels:
            travel_time = (travel.schedule+timedelta(hours=1)).strftime("%H:%M")
            travel_time_html_id_format = "hour" + travel_time.replace(":","")
            travel_times.append(travel_time)
            tickets_sold = Ticket.objects.filter(travel=travel)
            seats_sold = [ticket_sold.seat_number for ticket_sold in tickets_sold]
            buses.update({
                travel_time_html_id_format: (
                    travel.bus.seats,
                    (4-travel.bus.seats_first_row),
                    seats_sold,
                ),
            })
        context.update({"travel_times":travel_times,"buses":buses})
    else:
        errors = {key:value[0] for (key,value) in form.errors.items()}
        form_clean_error = errors.get("__all__")
        context.update({"errors":errors,"form_clean_error":form_clean_error})
            
    if request.POST["action"] == "Buy":
        form2 = PurchaseTicketForm(request.POST)
        if form2.is_valid():
            date = form2.cleaned_data["date"]
            time = form2.cleaned_data["time"]
            origin = form2.cleaned_data["origin"]
            destination = form2.cleaned_data["destination"]
            travel = Travel.objects.get(
                schedule__date = date,
                schedule__time = time,
                origin = origin,
                destination = destination,
            )
            # Price is test
            ticket_form = TicketForm({
                "user": request.user,
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
    context = {"user":request.user,}
    if request.POST.get("action") == "Cancel":
        last_ticket = Ticket.objects.filter(user=request.user).order_by("-purchase_datetime")[0]
        last_ticket.delete()
        return HttpResponseRedirect(reverse("booking:mytickets")) 
    elif request.POST.get("action") == "Confirm":
        return HttpResponseRedirect(reverse("booking:mytickets")) 
    else:
        last_ticket = Ticket.objects.filter(user=request.user).order_by("-purchase_datetime")[0]
        ten_seconds_ago = datetime.now() - timedelta(seconds=10)
        if get_object_or_404(Ticket,user=request.user,purchase_datetime__gt=ten_seconds_ago) == last_ticket:
            context.update({"ticket":last_ticket})
            return render(request,"booking/confirm_ticket.html",context)
        else:
            return HttpResponseRedirect(reverse("booking:mytickets"))

@login_required
def mytickets(request):
    context = {"user":request.user,}
    user_tickets = Ticket.objects.filter(user=request.user)
    active_tickets = user_tickets.filter(travel__schedule__gte=datetime.now()).order_by("travel__schedule")
    context.update({"active_tickets":active_tickets})
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

def singup(request):
    context = {"request":request.POST}
    if request.POST.get("action") == "Create account":
        form = SingupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username = data["username"],
                email = data["email"],
                password = data["new_password"],
                first_name = "None",
                last_name = "None",
            )
            customer = Customer(user=user)
            customer.save()
            return HttpResponseRedirect(reverse("booking:login"))
        else:
            errors = {key:value[0] for (key,value) in form.errors.items()}
            form_clean_error = errors.get("__all__")
            context.update({"errors":errors,"form_clean_error":form_clean_error})
            return render(request,"booking/singup.html",context)
    else:
        return render(request,"booking/singup.html",context)

def login_view(request,password_changed=None):
    context = {"request":request.POST}
    if request.POST.get("action") == "Submit":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("booking:travel"))
        else:
            context.update({"auth_failed":"An error ocurred, please revise username and password."})
    elif password_changed == "password":
        success_message = """
        Your password has been changed successfully. Please log in again with your new password.
        """
        context.update({"password_changed":success_message})
    return render(request,"booking/login.html",context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("booking:travel"))

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
                return HttpResponseRedirect(reverse(
                    "booking:login_new_password",
                    args=("password",)
                ))
            else:
                context.update({"incorrect_password":"Incorrect password"})
                return render(request,"booking/change_password.html",context)
        else:
            errors = {key:value[0] for (key,value) in form.errors.items()}
            context.update({"errors":errors})
            context.update({"not_same_password":errors.get("__all__")})
            return render(request,"booking/change_password.html",context)

    elif request.POST.get("action") == "Cancel":
        return HttpResponseRedirect(reverse("booking:profile"))

    return render(request,"booking/change_password.html",context)


@login_required
def ticket_information(request,ticket_id):
    context = {"user":request.user,}
    ticket = get_object_or_404(Ticket,pk=ticket_id)
    if ticket.user == request.user:
        context.update({"ticket":ticket})
        return render(request,"booking/ticket_information.html",context)
    else:
        return HttpResponseRedirect(reverse("booking:mytickets"))

@login_required
def ticket_cancel(request,ticket_id):
    context = {"user":request.user,}
    ticket = get_object_or_404(Ticket,pk=ticket_id)
    if ticket.user == request.user:
        now_utc = datetime.now(timezone(timedelta(0)))
        if ticket.travel.schedule < (now_utc + timedelta(days=1)):
            cancel_error = "You can not cancel tickets with less than one day remaining"
            context.update({"ticket":ticket,"cancel_error":cancel_error})
            return render(request,"booking/ticket_information.html",context)
        else:
            ticket.delete()
            return HttpResponseRedirect(reverse("booking:mytickets"))
    else:
        return HttpResponseRedirect(reverse("booking:mytickets"))