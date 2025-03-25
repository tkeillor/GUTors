from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views import View
from GUTors_app.forms import UserProfileForm, SearchForm, CreateSessionForm
from GUTors_app.models import *
from django.db.models import Avg
from django.db.models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def home(request):
    return render(request, 'GUTors_app/home.html')


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'bio': user_profile.bio,
                                'profile picture': user_profile.profile_picture,
                                'subjects': user_profile.subjects})
        return (user, user_profile, form)
    
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('GUTors:home'))
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'GUTors_app/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('GUtors:home'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('GUTors:profile', user.username)
        else:
            print(form.errors)
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'GUTors_app/profile.html', context_dict)



def profile_setup(request):
    profile = request.user.userprofile  # the related UserProfile for this user
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want to send the user next
    return render(request, 'profile_setup.html', {'form': form})



@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('GUTors:profile', user_profile.user.username)
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'GUTors_app/profile_registration.html', context_dict)


"""def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("/")"""

def logout(request):
    return render(request, 'GUTors_app/logout.html')

def register(request):
    return render(request, 'GUTors_app/register.html')

def profile(request):
    user_profile = request.user.userprofile
    reviews = Review.objects.filter(session__tutor=user_profile)
    avg_rating = reviews.aggregate(avg = Avg("rating"))["avg"] or 0
    subjects = user_profile.subjects.all()

    context = {
        'user_profile': user_profile,
        'reviews': reviews,
        'avg_rating' : avg_rating,
        'subjects' : subjects,
    }
    return render(request, 'GUTors_app/profile.html', context)

@login_required
def search(request):
    form = SearchForm(request.GET or None)
    results = None

    if form.is_valid():
        username = form.cleaned_data.get('username')
        subject = form.cleaned_data.get('subject')
        results = UserProfile.objects.all()
        if username:
            results = results.filter(user__username__icontains=username)
        if subject and not username:
            results = results.filter(subjects=subject)
    return render(request, 'GUTors_app/search.html', {'results':results, 'form':form})

def review(request):
    return render(request, 'GUTors_app/review.html')

def create_tutoring_session(request):
    form = CreateSessionForm()

    if request.method == 'POST':
        form = CreateSessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)
            session.tutor = request.user.userprofile
            session.save()

            return redirect(reverse('home'))
        else:
            print(form.errors)
    return render(request, 'GUTors_app/create_tutoring_session.html', {'form':form})