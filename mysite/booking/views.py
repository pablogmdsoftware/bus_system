from django.shortcuts import render

def about(request):
    context = {}
    return render(request,"booking/about.html",context)
