from django.shortcuts import render

def index(request):
    return render(request, 'GUTors_app/index.html')

def login(request):
    return render(request, 'GUTors_app/login.html')

def register(request):
    return render(request, 'GUTors_app/register.html')

def profile(request):
    return render(request, 'GUTors_app/profile.html')

def search(request):
    return render(request, 'GUTors_app/search.html')

def review(request):
    return render(request, 'GUTors_app/review.html')
