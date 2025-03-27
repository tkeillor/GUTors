from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from GUTors_app.models import UserProfile, Review, Subject, TutoringSession
from GUTors_app.forms import UserProfileForm

class ViewTests(TestCase):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        
        # Create a test user and profile
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user_profile = UserProfile.objects.create(user=self.user, bio="Test Bio", role="STUDENT")
        
        # Create a test subject and tutoring session
        self.subject = Subject.objects.create(name="Mathematics")
        self.user_profile.subjects.add(self.subject)
        
        self.session = TutoringSession.objects.create(
            tutor=self.user_profile,
            student=self.user_profile,
            subject=self.subject
        )

    def test_home_page_loads(self):
        """Ensure the home page loads successfully"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "GUTors_app/home.html")

    def test_profile_view_authenticated(self):
        """Check if a logged-in user can access their profile"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("GUTors:profile", kwargs={"username": "testuser"}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "GUTors_app/profile.html")
        self.assertEqual(response.context["user_profile"], self.user_profile)

    def test_profile_update(self):
        """Test updating user profile information"""
        self.client.login(username="testuser", password="password123")

        update_data = {"bio": "Updated Bio", "role": "TUTOR", "subjects": [self.subject.id]}
        response = self.client.post(reverse("GUTors:Register_profile"), update_data)

        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.bio, "Updated Bio")
        self.assertEqual(self.user_profile.role, "TUTOR")

    def test_search_functionality(self):
        """Test searching by username and subject"""
        self.client.login(username="testuser", password="password123")

        # Search by username
        response = self.client.get(reverse("GUTors:search"), {"username": "testuser"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

        # Search by subject
        response = self.client.get(reverse("GUTors:search"), {"subject": self.subject.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathematics")

    def test_review_submission(self):
        """Test leaving a review for a tutoring session"""
        self.client.login(username="testuser", password="password123")

        review_data = {"rating": 4, "comment": "Great session!"}
        response = self.client.post(reverse("GUTors:review_session", kwargs={"session_id": self.session.id}), review_data)

        review = Review.objects.filter(session=self.session).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Great session!")

    def test_create_tutoring_session(self):
        """Test creating a new tutoring session"""
        self.client.login(username="testuser", password="password123")

        session_data = {
            "subject": self.subject.id,
            "description": "Test tutoring session",
            "date": "2024-06-15",
            "start_time": "14:00",
            "end_time": "15:00"
        }

        response = self.client.post(reverse("create_session"), session_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertTrue(TutoringSession.objects.filter(tutor=self.user_profile, subject=self.subject).exists())



#response status codes for unit tests 
# 1xx - Informational
# 100: Continue - Request received, continue sending
# 101: Switching Protocols - Server switching to another protocol

# 2xx - Success
# 200: OK - Request successful
# 201: Created - Resource created successfully
# 204: No Content - Request successful, but no content to return

# 3xx - Redirection
# 301: Moved Permanently - Resource permanently moved
# 302: Found - Temporary redirect
# 304: Not Modified - Cached version is valid

# 4xx - Client Errors
# 400: Bad Request - Invalid request syntax
# 401: Unauthorized - Authentication required
# 403: Forbidden - Permission denied
# 404: Not Found - Resource does not exist
# 405: Method Not Allowed - HTTP method not allowed

# 5xx - Server Errors
# 500: Internal Server Error - Unexpected server issue
# 502: Bad Gateway - Invalid response from upstream server
# 503: Service Unavailable - Server overloaded or down
# 504: Gateway Timeout - Upstream server took too long to respond