from django.urls import path
from GUTors_app import views

app_name = 'GUTors'

urlpatterns = [
    path('', views.index, name='index')
]