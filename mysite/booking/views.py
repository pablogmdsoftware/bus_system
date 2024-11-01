from django.shortcuts import render

def about(request):
    context = {}
    render(request,"booking/about.html",context)
