from django.urls import include, path
from GUTors_app import views


app_name = 'GUTors'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('review/', views.review, name='review'),
    path('profile/<username>/', views.profile, name='profile'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('create_tutoring_session', views.create_tutoring_session, name = 'create_tutoring_session'),
    path('session/<int:session_id>/review/', views.review_session, name='review_session'),
    path('session/<int:id>/', views.join_session, name='session')
    #path('booking/', views.booking, name='booking'),
]