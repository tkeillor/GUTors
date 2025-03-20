from django.contrib import admin
from django.urls import path
from django.urls import include
from GUTors_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('rango/', include('GUTors_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.backends.simple.urls'))
]
