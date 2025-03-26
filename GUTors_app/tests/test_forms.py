from django.test import TestCase
from GUTors_app.models import Subject, UserProfile
from GUTors_app.forms import SearchForm, ReviewForm, TutoringSessionForm, UserProfileForm, CreateSessionForm
from django.contrib.auth.models import User



class TestUserProfileForm(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
    
    def test_valid_user(self):
        form = UserProfileForm(data={
            'role':'TUTOR',
            'bio': "I'm the best tutor",
            'profile_picture':'',
            'subjects':[]
        })
        self.assertTrue(form.is_valid()) # Basic profile form like this should be valid
        
    def test_invalid_user_no_role(self):
        form = UserProfileForm(data={
            'bio': "I'm the best tutor",
            'profile_picture':'',
            'subjects':[]
        })
        self.assertFalse(form.is_valid()) # Profile form without role should'nt be valid
        
    def test_invalid_user_wrong_role(self):
        form = UserProfileForm(data={
            'role':'BATMAN',
            'bio': "I'm the best tutor",
            'profile_picture':'',
            'subjects':[]
        })
        self.assertFalse(form.is_valid()) # Unfortunatly Batman won't be tutoring or taking any classes :(
            
class TestTutoringSessionForm(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Mathematics")
    
    def test_valid_tutor_session_form(self):
        form = TutoringSessionForm(data={
            'subject': self.subject.id,
            'title': 'Maths',
            'date': '2025-05-17 10:00'
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
    
class TestReviewForm(TestCase):
    
    def test_valid_review_form(self):
        form = ReviewForm(data={
            'rating':5,
            'comment': 'Great session, very useful'
        })
        self.assertTrue(form.is_valid())
    
    def test_invalid_review_no_comment_on_form(self):
        form = ReviewForm(data={
            'rating':5
        })
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)
        
    def test_invalid_review_form_invalid_rating(self):
        form = ReviewForm(data={
            'rating':10,
            'comment': 'Great Session, very useful'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        
class TestSearchForm(TestCase):
    
    def test_valid_search_form(self):
        form = SearchForm(data={})
        self.assertTrue(form.is_valid())
    
class TestCreateSessionForm(TestCase):
    def setUp(self):
        self.subject =Subject.objects.create(name="Physics")
    
    def test_valid_create_session_form(self):
        form = CreateSessionForm(data={
            'subject':self.subject.id,
            'title': 'Physics',
            'date': '2025-05-25T12:00'
        })
        self.assertTrue(form.is_valid())