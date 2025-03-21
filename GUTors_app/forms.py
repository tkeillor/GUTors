from django import forms
from django.contrib.auth.models import User
from GUTors_app.models import TutoringSession, Review, UserProfile




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'bio', 'profile_picture', 'subjects']


class TutoringSessionForm(forms.ModelForm):
    class Meta:
        model = TutoringSession
        exclude = ('tutor', 'student')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')