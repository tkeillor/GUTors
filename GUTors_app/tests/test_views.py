from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from GUTors_app.models import UserProfile, Review, Subject
from GUTors_app.forms import UserProfileForm

class TestHomePage(SimpleTestCase):
    
    """Testing if homepage returns HTTP 200 response"""
    def test_homepage_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
class TestProfileView(TestCase):
    def setUp(self):
        '''Creating test user'''
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='ExamplePassword123')
        self.subject = Subject.objects.create(name="Mathematics")
        self.user_profile = UserProfile.objects.create(user=self.user, bio="Test Bio")
        self.user_profile.subjects.add(self.subject)

        
    def test_profile_view_logged_in(self):
        #profile page should load correctly for logged in users
        self.client.login(username='testuser', password='ExamplePassword123')
        response = self.client.get(reverse('GUTors:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'GUTors_app/profile.html')
        self.assertContains(response, "Test Bio")
        
    def test_post_profile_update(self):
        self.client.login(username='testuser', password='ExamplePassword123')
        response = self.client.post(
            reverse('GUTors:profile', kwargs={'username': 'testuser'}),
            {'bio': 'Updated Bio', 'role': 'STUDENT'}
        )
        self.assertEqual(response.status_code,200)#Redirects user after successful form submission
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.bio, 'Updated Bio')  
        print(response.content.decode())     
        
    def test_register_profile_exists(self):
        self.client.login(username='testuser', password='ExamplePassword123')
        response = self.client.get(reverse('GUTors:Register_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GUTors_app/profile_registration.html')
        
class TestSearchView(TestCase):
    def setUp(self):
        self.client = Client()
        self.subject = Subject.objects.create(name="Physics")
        self.user = User.objects.create_user(username="physics_tutor", password="password")
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.user_profile.subjects.add(self.subject)
            
    def test_search_by_username(self):
        response = self.client.get(reverse('GUTors:search'), {'username': 'physics_tutor'})  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "physics_tutor") 
        
    def test_searhc_by_subject(self):
        
        response = self.client.get(reverse('GUTors:Search'), {'subject':self.subject.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Physics")



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