from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .userform import RegistrationForm
from .models import User

def profilepage(request):
    context = {}
    return render(request, 'MyReviews/userprofile.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    if not request.POST:
        context = {}
        return render(request, 'MyReviews/loginpage.html', context)
    
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'User does not exist')
    
    user = authenticate(username=username, password=password)

    if user is None:
        messages.error(request, 'Username or Password does not exist.')
    
    login(request, user)
    return redirect('home-page')

def logoutrequest(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    
    logout(request)
    return redirect('home-page')

def registerpage(request):
    form = RegistrationForm

    if not request.POST:
        context = {'form': form}
        return render(request, 'MyReviews/registerpage.html', context)
    
    form = RegistrationForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('login-page')
    else:
        message = "Form was invalid"
        context = {'message': message, 'form': form}
        return render(request, 'MyReviews/registerpage.html', context)
    