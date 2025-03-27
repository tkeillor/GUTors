from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views import View
from GUTors_app.forms import UserProfileForm, SearchForm, CreateSessionForm, JoinSessionForm, ReviewForm
from GUTors_app.models import *
from django.db.models import Avg
from django.db.models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def home(request):
    return render(request, 'GUTors_app/home.html')


from django.contrib import messages
from django.http import HttpResponseRedirect

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        try:
            # Try to get the existing profile
            user_profile = UserProfile.objects.get(user=user)
            form = UserProfileForm({'bio': user_profile.bio,
                                   'profile picture': user_profile.profile_picture,
                                   'subjects': user_profile.subjects})
            return (user, user_profile, form)
        except UserProfile.DoesNotExist:
            # Profile doesn't exist - we'll handle this in the view methods
            return (user, None, None)
    
    @method_decorator(login_required)
    def get(self, request, username):
        result = self.get_user_details(username)
        
        if result is None:
            messages.error(request, f"User '{username}' does not exist.")
            return redirect(reverse('GUTors:home'))
            
        user, user_profile, form = result
        
        # If profile doesn't exist
        if user_profile is None:
            # If this is the current user, redirect to profile creation
            if request.user.username == username:
                return redirect('GUTors:register_profile')
            else:
                # If it's someone else's profile, show error message
                messages.error(request, f"The user '{username}' has not created a profile yet.")
                return redirect(reverse('GUTors:home'))

        reviews = Review.objects.filter(session__tutor=user_profile)
        avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0
        subjects = user_profile.subjects.all()
        print(f"Subjects for {user_profile.user.username}: {list(subjects)}")
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'reviews': reviews,
                        'avg_rating': avg_rating,
                        'subjects': subjects,
                        'form': form}
        return render(request, 'GUTors_app/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        # Check if this is the user's own profile
        if request.user.username != username:
            messages.error(request, "You can only edit your own profile.")
            return redirect(reverse('GUTors:home'))
            
        result = self.get_user_details(username)
        
        if result is None:
            messages.error(request, f"User '{username}' does not exist.")
            return redirect(reverse('GUTors:home'))
            
        user, user_profile, form = result
        
        # If profile doesn't exist
        if user_profile is None:
            return redirect('GUTors:register_profile')
            
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
    try:
        # Try to get existing profile
        user_profile = UserProfile.objects.get(user=request.user)
        # If we get here, the profile exists - we're editing
        is_edit = True
    except UserProfile.DoesNotExist:
        # Profile doesn't exist - we're creating new
        user_profile = None
        is_edit = False
    
    if request.method == 'POST':
        if is_edit:
            # Editing existing profile
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            # Creating new profile
            form = UserProfileForm(request.POST, request.FILES)
            
        if form.is_valid():
            if not is_edit:
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
                form.save_m2m()
            else:
                form.save()
                
            return redirect('GUTors:profile', user_profile.user.username)
        else:
            print(form.errors)
    else:
        if is_edit:
            form = UserProfileForm(instance=user_profile)
        else:
            form = UserProfileForm()
    
    context_dict = {
        'form': form, 
        'is_edit': is_edit
    }
    return render(request, 'GUTors_app/profile_registration.html', context_dict)

def register(request):
    return render(request, 'GUTors_app/register.html')

def profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    tutor_reviews = Review.objects.filter(session__tutor=user_profile)
    student_reviews = Review.objects.filter(session__student=user_profile)
    avg_rating = round(tutor_reviews.aggregate(avg = Avg("rating"))["avg"] or 0,1)
    subjects = user_profile.subjects.all()
    tutor_sessions = TutoringSession.objects.all().filter(tutor=user_profile)
    student_sessions = TutoringSession.objects.all().filter(student=user_profile)

    context = {
        'user_profile': user_profile,
        'tutor_reviews': tutor_reviews,
        'student_reviews':student_reviews,
        'avg_rating' : avg_rating,
        'subjects' : subjects,
        'tutor_sessions' : tutor_sessions,
        'student_sessions': student_sessions
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

@login_required
def review_session(request, session_id):
    # Get the session object
    session = get_object_or_404(TutoringSession, id=session_id)
    user_profile = request.user.userprofile
    
    # Security check: make sure the user is the student in this session
    if session.student != user_profile:
        return redirect('GUTors:home')
    
    # Check if a review already exists for this session
    try:
        existing_review = Review.objects.get(session=session)
        form = ReviewForm(instance=existing_review)
        is_edit = True
    except Review.DoesNotExist:
        form = ReviewForm()
        is_edit = False
    
    # Get all reviews by this user for display
    reviews = Review.objects.filter(session__student=user_profile)
    
    if request.method == "POST":
        if is_edit:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)
            
        if form.is_valid():
            review = form.save(commit=False)
            review.session = session
            review.save()
            return redirect('GUTors:profile', session.tutor.user.username)
    
    return render(request, 'GUTors_app/review.html', {
        'session': session,
        'sessions': [session],  # For compatibility with existing template
        'reviews': reviews,
        'form': form,
        'is_edit': is_edit
    })


@login_required
def review(request):
    user_profile = request.user.userprofile
    sessions = TutoringSession.objects.filter(student=user_profile)
    reviews = Review.objects.filter(session__student=user_profile)
    form = ReviewForm()
    
    return render(request, 'GUTors_app/review.html', {
        'sessions': sessions,
        'reviews': reviews,
        'form': form
    })

def create_tutoring_session(request):
    form = CreateSessionForm()

    if request.method == 'POST':
        form = CreateSessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)
            session.tutor = request.user.userprofile
            session.save()

            return redirect('GUTors:session', session.id)
        else:
            print(form.errors)
    return render(request, 'GUTors_app/create_tutoring_session.html', {'form':form})

def join_session(request, id):
    session = get_object_or_404(TutoringSession, id=id)
    form = JoinSessionForm()

    if request.method == 'POST':
        form = JoinSessionForm(request.POST)
        if form.is_valid():
            session.student = request.user.userprofile
            session.save()
    
    context = {
        'session':session,
        'form':form
    }
    
    return render(request, 'GUTors_app/session.html',context)


