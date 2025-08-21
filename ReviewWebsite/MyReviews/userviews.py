from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import User

def profilepage(request):
    context = {}
    return render(request, 'MyReviews/userprofile.html', context)

def loginpage(request):
    context = {}
    return render(request, 'MyReviews/loginpage.html', context)

def registerpage(request):
    context = {}
    return render(request, 'MyReviews/registerpage.html', context)