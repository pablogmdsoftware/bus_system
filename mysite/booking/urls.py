from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path("", views.travel, name="travel"),
    path("travel/", views.travel, name="travel"),
    path("travel/buy/", views.select_ticket, name="buy"),
    path("travel/buy/confirm/", views.confirm_ticket, name="confirm"),
    path("mytickets/", views.mytickets, name="mytickets"),
    path("mytickets/<int:ticket_id>/", views.ticket_information, name="ticket_information"),
    path("mypasses/", views.mypasses, name="mypasses"),
    path("about/", views.about, name="about"),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/profile/password/", views.change_password, name="password"),
    path("accounts/singup/", views.singup, name="singup"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/login/<str:password_changed>/", views.login_view, name="login_new_password"),
    path("accounts/logout/", views.logout_view, name="logout"),
]