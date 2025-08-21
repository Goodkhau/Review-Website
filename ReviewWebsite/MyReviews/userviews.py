from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .userform import RegistrationForm

def profilepage(request):
    context = {}
    return render(request, 'MyReviews/userprofile.html', context)

def loginpage(request):
    context = {}
    return render(request, 'MyReviews/loginpage.html', context)

def registerpage(request):
    form = RegistrationForm()

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
    