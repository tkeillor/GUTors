# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator




from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = (('STUDENT', 'Student'), ('TUTOR', 'Tutor'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to core User
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='STUDENT')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)  # link to Subject model (for tutors)

    def __str__(self):
        return self.user.username


class TutoringSession(models.Model):
    tutor = models.ForeignKey(UserProfile, related_name='tutoring_session_as_tutor',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()     
    student = models.ForeignKey(UserProfile, null=True, related_name='tutoring_session_as_student', blank=True, on_delete=models.SET_NULL)
    def __str__(self): 
        status = "Booked" if self.student else "Available"
        return f"{self.subject.name} on {self.date:%Y-%m-%d %H:%M} ({status})"

class Review(models.Model):
    session = models.OneToOneField(TutoringSession, on_delete=models.CASCADE, blank=True)
    # One review per session (one student per session)
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])  # 1-5
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return f"Review for {self.session.tutor.user.username} by {self.session.student.user.username}: {self.rating}/5"