from django.test import TestCase
from GUTors_app.models import UserProfile, Subject, TutoringSession, Review
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import make_aware


class TestSubjectModel(TestCase):
    #Testing that it can create subjects
    def test_create_subject(self):
        subject = Subject.objects.create(name="Mathematics")
        self.assertEqual(str(subject), "Mathematics")
        
class TestUserProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='ExamplePassword123')
        
    def test_create_user_profile(self):
        profile = UserProfile.objects.create(user=self.user, bio="Tutoring is the best")
        self.assertEqual(str(profile), "testuser")
        self.assertEqual(profile.role, "STUDENT") # Student is the default
        
    def add_subject_to_tutor(self):
        print("Test to be written")
        profile = UserProfile.objects.create(user=self.user, role="TUTOR")
        subject = Subject.objects.create(name="Physics")
        profile.subjects.add(subject)
        self.assertIn(subject, profile.subjects.all())
        
    def test_tutoring_session_creation(self):
        print("Session created test needs implementing")
        
    def test_tutoring_session_booking(self):
        print("Session booked test needs implenting")
        
class TestReviewModel(TestCase):
    def setUp(self):
        self.tutor_user = User.objects.create_user(username='tutor2', password="ExamplePassword123")
        self.student_user = User.objects.create_user(username="student2", password="ExamplePassword123")
        self.tutor_profile = UserProfile.objects.create(user=self.tutor_user, role = "TUTOR")
        self.student_profile = UserProfile.objects.create(user=self.student_user, role = "STUDENT")
        self.subject = Subject.objects.create(name="Chemistry")
        self.session = TutoringSession.objects.create(
            tutor=self.tutor_profile,
            subject=self.subject,
            title = "Physical Chemistry",
            date=make_aware(datetime(2025,6,14,0)),
            student=self.student_profile
            
            
        )
        
    def test_create_review(self):
        review=Review.objects.create(session=self.session, rating=4,comment="Very useful tutoring, thumbd up man :)")
        self.assertEqual(review.rating, 4)
        self.assertEqual(str(review), "Review for tutor2 by student2: 4/5")