from django.shortcuts import render

def travel(request):
    context = {}
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