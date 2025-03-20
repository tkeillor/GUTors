from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'GUTors_app/home.html')

def login(request):
    '''if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("/")'''
    return render(request, 'GUTors_app/login.html')

def logout(request):
    return render(request, 'GUTors_app/logout.html')

def register(request):
    return render(request, 'GUTors_app/register.html')

def profile(request):
    return render(request, 'GUTors_app/profile.html')

def search(request):
    return render(request, 'GUTors_app/search.html')

def review(request):
    return render(request, 'GUTors_app/review.html')
