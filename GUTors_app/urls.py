from django.urls import path
from GUTors_app import views

app_name = 'GUTors'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='regiser'),
    path('search/', views.search, name='search'),
    path('review/', views.review, name='review'),
    path('profile/', views.profile, name='profile'),
    path('booking/', views.booking, name='booking')
]