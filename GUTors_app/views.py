from django.shortcuts import render
from django.shortcuts import get_object_or_404
from GUTors_app.models import *
from django.db.models import Avg
from django.db.models import *
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
    user_profile = get_object_or_404(UserProfile,user=2)
    reviews = Review.objects.filter(session__tutor=user_profile)
    avg_rating = reviews.aggregate(Avg("rating", default=0))
    subjects = Subject.objects.all()

    context = {
        'user_profile': user_profile,
        'reviews': reviews,
        'avg_rating' : avg_rating,
        'subjects' : subjects,
    }
    return render(request, 'GUTors_app/profile.html', context)

def search(request):
    return render(request, 'GUTors_app/search.html')

def review(request):
    return render(request, 'GUTors_app/review.html')
