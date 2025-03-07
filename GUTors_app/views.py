from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("HOMEPAGE")

def login(request):
    return HttpResponse("GUTors says hey there partner")

def register(request):
    return HttpResponse("GUTors says hey there partner")

def profile(request):
    return HttpResponse("GUTors says hey there partner")

def search(request):
    return HttpResponse("GUTors says hey there partner")

def review(request):
    return HttpResponse("GUTors says hey there partner")