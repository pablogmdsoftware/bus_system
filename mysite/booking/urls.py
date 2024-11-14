from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path("", views.travel, name="travel"),
    path("travel/", views.travel, name="travel"),
    path("travel/buy/", views.select_ticket, name="buy"),
    path("travel/buy/confirm/", views.confirm_ticket, name="confirm"),
    path("mytickets/", views.mytickets, name="mytickets"),
    path("mypasses/", views.mypasses, name="mypasses"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("singin/", views.singin, name="singin"),
]