from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from GUTors_app.models import TutoringSession, Review, UserProfile, Subject




class UserProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = UserProfile
        fields = ['role', 'bio', 'profile_picture', 'subjects']


class TutoringSessionForm(forms.ModelForm):
    class Meta:
        model = TutoringSession
        exclude = ('tutor', 'student')

class ReviewForm(forms.ModelForm):

    rating =forms.ChoiceField(
        choices=[(1,"1/5"),(2,"2/5"),(3,"3/5"),(4,"4/5"),(5,"5/5")],
         required=True,
         widget= forms.Select(attrs={'class': 'form-control'})
     )

    class Meta:
        model = Review
        fields = ('rating', 'comment')


class SearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter tutor username'})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="Select a subject",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    search_type = forms.ChoiceField(
        choices=[('tutors', 'Search for Tutors'), ('sessions', 'Search for Sessions')],
        initial='tutors',
        widget=forms.RadioSelect()
    )
    

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
        
    def clean_date(self):
        """Ensure the date is not in the past"""
        selected_date = self.cleaned_data.get('date')
        
        if selected_date and selected_date < timezone.now():
            raise ValidationError("You cannot schedule a session in the past")
        
        return selected_date


class JoinSessionForm(forms.ModelForm):
    class Meta:
        model = TutoringSession
        fields = ('student',)


