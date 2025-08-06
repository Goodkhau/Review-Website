from django.shortcuts import render

def home(request):
    return render(request, 'MyReviews/home.html')