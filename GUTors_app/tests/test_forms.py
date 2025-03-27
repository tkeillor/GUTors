from django.test import TestCase
from django.contrib.auth.models import User
from GUTors_app.models import Subject
from GUTors_app.forms import (
    UserProfileForm, 
    TutoringSessionForm, 
    ReviewForm, 
    SearchForm, 
    CreateSessionForm
)
from datetime import datetime, timedelta

class FormTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.subject = Subject.objects.create(name="Mathematics")
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_user_profile_form_valid(self):
        """Test UserProfileForm with valid data"""
        form_data = {
            "role": "TUTOR",
            "bio": "Experienced math tutor",
            "subjects": [self.subject.id],
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_missing_role(self):
        """Test UserProfileForm without a role (should be invalid)"""
        form_data = {
            "bio": "Experienced math tutor",
            "subjects": [self.subject.id],
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_profile_form_invalid_role(self):
        """Test UserProfileForm with an invalid role (should be invalid)"""
        form_data = {
            "role": "Batman",  # Invalid role, Batman doesn't need tutoring
            "bio": "Experienced math tutor",
            "subjects": [self.subject.id],
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_tutoring_session_form_valid(self):
        """Test TutoringSessionForm with valid data"""
        form_data = {
            "subject": self.subject.id,
            "title": "Math Tutoring",
            "date": datetime.now() + timedelta(days=1),
        }
        form = TutoringSessionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_tutoring_session_form_missing_subject(self):
        """Test TutoringSessionForm without a subject (should be invalid)"""
        form_data = {
            "title": "Math Tutoring",
            "date": datetime.now() + timedelta(days=1),
        }
        form = TutoringSessionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_review_form_valid(self):
        """Test ReviewForm with valid data"""
        form_data = {
            "rating": 4,
            "comment": "Very helpful session!",
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_missing_comment(self):
        """Test ReviewForm without a comment (should be invalid)"""
        form_data = {"rating": 5}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("comment", form.errors)

    def test_review_form_invalid_rating(self):
        """Test ReviewForm with an out-of-range rating (should be invalid)"""
        form_data = {
            "rating": 10,  # Out of range
            "comment": "Test comment",
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_search_form_valid(self):
        """Test SearchForm with different valid inputs"""
        self.assertTrue(SearchForm(data={}).is_valid())  # Empty form should be valid

        form_data = {"username": "testuser"}
        self.assertTrue(SearchForm(data=form_data).is_valid())

        form_data = {"subject": self.subject.id}
        self.assertTrue(SearchForm(data=form_data).is_valid())

    def test_create_session_form_valid(self):
        """Test CreateSessionForm with valid data"""
        form_data = {
            "subject": self.subject.id,
            "title": "Advanced Mathematics",
            "date": datetime.now() + timedelta(days=1),
        }
        form = CreateSessionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_session_form_missing_title(self):
        """Test CreateSessionForm without a title (should be invalid)"""
        form_data = {
            "subject": self.subject.id,
            "date": datetime.now() + timedelta(days=1),
        }
        form = CreateSessionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_session_form_past_date(self):
        """Test CreateSessionForm with a past date (should be invalid)"""
        form_data = {
            "subject": self.subject.id,
            "title": "Past Session",
            "date": datetime.now() - timedelta(days=1),
        }
        form = CreateSessionForm(data=form_data)
        self.assertFalse(form.is_valid())  # Assuming form validation prevents past dates
