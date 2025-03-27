import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'GUTors.settings')

import django
django.setup()
from GUTors_app.models import Subject, TutoringSession, Review, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


def populate():

    subjects = [{"name":"Maths"},
            {"name":"Computer Science"},
            {"name":"Physics"},
            {"name":"Economics"},
            {"name":"Business"},
            {"name":"Engineering"},
            {"name":"Chemistry"}]
    
    for subject in subjects:
        add_subject(subject["name"])

    users = [{"username":"tkeillor",
              "first_name":"Thomas",
              "last_name":"Keillor",
              "email":"thomaskeillor@gmail.com",
              "role":"TUTOR",
              "bio":"Im Thomas, I'm a for Maths and Computer Science!",
              "subjects":["Maths","Computer Science"],
              "profile_picture":"{% static 'images/frasergrahempfp.jpg' %}"},

              {"username":"dgong",
              "first_name":"Daibo",
              "last_name":"Gong",
              "email":"daibogong@gmail.com",
              "role":"STUDENT",
              "bio":"Im Daibo",
              "subjects":["Maths","Computer Science"],
              "profile_picture":"{% static 'images/frasergrahempfp.jpg' %}"
              },

              {"username":"fgraham",
              "first_name":"Fraser",
              "last_name":"Graham",
              "email":"frasergraham@gmail.com",
              "role":"STUDENT",
              "bio":"Im Fraser",
              "subjects":["Physics", "Chemistry", "Maths"],
              "profile_picture":"{% static 'images/avatar.jpg' %}"},
              
              {"username":"gedwards",
              "first_name":"Gareth",
              "last_name":"Edwards",
              "email":"garethedwards@gmail.com",
              "role":"STUDENT",
              "bio":"Im Gareth",
              "subjects":["Maths","Computer Science"],
              "profile_picture":"{% static 'images/frasergrahempfp.jpg' %}"},
              
              {"username":"pkrawczuk",
              "first_name":"Patryk",
              "last_name":"Krawczuk",
              "email":"patrykkrawczuk@gmail.com",
              "role":"TUTOR",
              "bio":"Im Patryk",
              "subjects":["Maths","Computer Science"],
              "profile_picture":"{% static 'images/frasergrahempfp.jpg' %}"},]
    
    for user in users:
        add_user(user["username"], user["first_name"], user["last_name"], user["email"], user["role"], user["bio"], user["subjects"], user["profile_picture"])

    tutoringSessions = [{"title":"Thomas Tutors Daibo",
                         "date":datetime(2025, 3, 13).date(),
                         "tutor":"tkeillor",
                         "student":"dgong",
                         "subject":"Maths",},
                         
                         {"title":"Thomas Tutors Gareth",
                         "date":datetime(2025, 3, 17).date(),
                         "tutor":"tkeillor",
                         "student":"gedwards",
                         "subject":"Maths",},
                         
                         {"title":"Patryk Tutors Thomas",
                         "date":datetime(2025, 3, 15).date(),
                         "tutor":"pkrawczuk",
                         "student":"tkeillor",
                         "subject":"Economics",}]
    
    for sesh in tutoringSessions:
        add_session(sesh["title"], sesh["date"], sesh["tutor"], sesh["student"], sesh["subject"])

    reviews = [{"session":"Thomas Tutors Daibo", 
                "rating":1,
                "comment":"Thomas is a terrible tutor. DO NOT CHOOSE HIM.",
                "date":datetime(2025, 3, 13).date()},
                
                {"session":"Thomas Tutors Gareth", 
                "rating":3,
                "comment":"This Thomas kid is mid af",
                "date":datetime(2025, 3, 17).date()},
                
                {"session":"Patryk Tutors Thomas", 
                "rating":5,
                "comment":"Is Patryk the goat?",
                "date":datetime(2025, 3, 16).date()},]
    
    for review in reviews:
        rev = add_review(review["rating"], review["comment"], review['session'], review['date'])



def add_user(username, first_name, last_name, email, role, bio, subjects, profile_picture):
    user = User.objects.create_user(username, email = email, first_name = first_name, last_name =last_name)
    u = UserProfile.objects.get_or_create(user = user, role = role, bio = bio, profile_picture=profile_picture)[0]
    for subject in subjects:
        s = Subject.objects.get(name=subject)
        u.subjects.add(s)
    u.save()
    return u

def add_subject(name):
    sub = Subject.objects.get_or_create(name = name)[0]
    sub.save()
    return sub

def add_session(title, date, tutor, student, subject):
    sesh = TutoringSession.objects.get_or_create(tutor = UserProfile.objects.get(user__username=tutor), student = UserProfile.objects.get(user__username=student), subject = Subject.objects.get(name=subject), title = title, date = timezone.make_aware(datetime.combine(date, datetime.min.time())))[0]
    sesh.save()
    return sesh

def add_review(rating, comment, session, date):
    r = Review.objects.get_or_create(rating = rating, comment = comment, session = TutoringSession.objects.get(title = session), created_at = timezone.make_aware(datetime.combine(date, datetime.min.time())))[0]
    r.save()
    return r

if __name__ == '__main__':
    print('Starting GUTors population script...')
    populate()