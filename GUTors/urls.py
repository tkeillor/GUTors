from django.contrib import admin
from django.urls import path
from django.urls import include
from GUTors import settings
from GUTors_app import views
from registration.backends.simple.views import RegistrationView
from django.urls import reverse
from django.conf.urls.static import static

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('GUTors:register_profile')


urlpatterns = [
    path('', views.home, name='home'),
    path('GUTors/', include('GUTors_app.urls')),
    path('accounts/register/',
        MyRegistrationView.as_view(),
        name='registration_register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
