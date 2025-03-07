from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("GUTors says hey there partner")