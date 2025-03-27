import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'GUTors.settings')

import django
django.setup()
from GUTors_app.models import Subject, TutoringSession, Review, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import shutil
from django.conf import settings
from django.core.files import File


def move_static_to_media(filename, static_subdir="images", media_subdir="profile_images"):
    static_path = os.path.join(settings.BASE_DIR, "static", static_subdir, filename)
    media_path = os.path.join(settings.MEDIA_ROOT, media_subdir, filename)

    os.makedirs(os.path.dirname(media_path), exist_ok=True)

    if os.path.exists(static_path):
        shutil.move(static_path, media_path)
        print(f"Moved {filename} from static to media.")
        return media_path
    else:
        print(f"File {static_path} does not exist.")
        return None


def populate():

    move_static_to_media('avatar.jpg')

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
              "bio":"I'm Thomas, I'm a tutor for Maths and Computer Science!",
              "subjects":["Maths","Computer Science"],
              "profile_picture":'tkeillorpfp.jpg'},

              {"username":"dgong",
              "first_name":"Daibo",
              "last_name":"Gong",
              "email":"daibogong@gmail.com",
              "role":"STUDENT",
              "bio":"I'm Daibo, I'm a student studying maths and chemistry. Looking for help from tutors.",
              "subjects":["Maths","Chemistry","Business"],
              "profile_picture":'dgongpfp.jpg'
              },

              {"username":"fgraham",
              "first_name":"Fraser",
              "last_name":"Graham",
              "email":"frasergraham@gmail.com",
              "role":"STUDENT",
              "bio":"I'm Fraser. I'm studying physics, chemisty, and maths. Help me please!!!",
              "subjects":["Physics", "Chemistry", "Maths"],
              "profile_picture":'fgrahampfp.jpg'},
              
              {"username":"gedwards",
              "first_name":"Gareth",
              "last_name":"Edwards",
              "email":"garethedwards@gmail.com",
              "role":"STUDENT",
              "bio":"I'm Gareth, love economics, need help with compsci",
              "subjects":["Economics","Computer Science"],
              "profile_picture":'gedwardspfp.jpg'},
              
              {"username":"pkrawczuk",
              "first_name":"Patryk",
              "last_name":"Krawczuk",
              "email":"patrykkrawczuk@gmail.com",
              "role":"TUTOR",
              "bio":"I'm Patryk, I can help you with anything.",
              "subjects":["Maths","Computer Science","Physics","Chemistry","Economics","Business","Engineering"],
              "profile_picture":'pkrawczukpfp.jpg'},]
    
    for user in users:
        add_user(user["username"], user["first_name"], user["last_name"], user["email"], user["role"], user["bio"], user["subjects"], user["profile_picture"])

    tutoringSessions = [{"title":"Thomas Teaches Daibo Maths",
                         "date":datetime(2025, 3, 13).date(),
                         "tutor":"tkeillor",
                         "student":"dgong",
                         "subject":"Maths",},
                         
                         {"title":"Thomas Tutors Gareth Computer Science",
                         "date":datetime(2025, 3, 17).date(),
                         "tutor":"tkeillor",
                         "student":"gedwards",
                         "subject":"Computer Science",},
                         
                         {"title":"Patryk Tutors Fraser Economics",
                         "date":datetime(2025, 3, 15).date(),
                         "tutor":"pkrawczuk",
                         "student":"fgraham",
                         "subject":"Economics",}]
    
    for sesh in tutoringSessions:
        add_session(sesh["title"], sesh["date"], sesh["tutor"], sesh["student"], sesh["subject"])

    reviews = [{"session":"Thomas Teaches Daibo Maths", 
                "rating":1,
                "comment":"Thomas is a terrible tutor. DO NOT CHOOSE HIM.",
                "date":datetime(2025, 3, 13).date()},
                
                {"session":"Thomas Tutors Gareth Computer Science", 
                "rating":3,
                "comment":"This Thomas kid is mid af",
                "date":datetime(2025, 3, 17).date()},
                
                {"session":"Patryk Tutors Fraser Economics", 
                "rating":5,
                "comment":"Is Patryk the goat?",
                "date":datetime(2025, 3, 16).date()},]
    
    for review in reviews:
        add_review(review["rating"], review["comment"], review['session'], review['date'])



def add_user(username, first_name, last_name, email, role, bio, subjects, profile_picture):
    user = User.objects.create_user(username, email = email, first_name = first_name, last_name =last_name)
    u = UserProfile.objects.get_or_create(user = user, role = role, bio = bio)[0]

    sample_file = os.path.join(settings.STATIC_DIR, 'images', profile_picture)
    with open(sample_file, 'rb') as f:
        u.profile_picture.save(profile_picture, File(f))
    
    for subject in subjects:
        s = Subject.objects.get(name=subject)
        u.subjects.add(s)
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