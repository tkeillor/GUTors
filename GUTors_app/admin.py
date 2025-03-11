from django.contrib import admin
from GUTors_app.models import Subject, UserProfile, TutoringSession, Review

admin.site.register(Subject)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(TutoringSession)
