from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from GUTors_app.models import TutoringSession, Review, UserProfile, Subject




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

class CreateSessionForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset = Subject.objects.all(),
        empty_label="Select a subject",
        required = False,
        widget= forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(max_length=200, help_text="Enter session title: ")
    date = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = TutoringSession
        exclude = ('tutor','student')
