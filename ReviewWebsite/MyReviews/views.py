from django.shortcuts import render, redirect
from .models import Movie, Review, Genre, User

def homepage(request):
    movies = Movie.objects.all().order_by('-release_date')[:10]
    reviews = Review.objects.all().order_by('-created_at')[:10]
    context = {'movies': movies, 'reviews': reviews}
    return render(request, 'MyReviews/homepage.html', context)

def genrepage(request):
    genre = Genre.objects.get(id=pk)
    context = {'genre': genre}
    return render(request, 'MyReviews/genrepage.html', context)

def chartpage(request):
    return render(request, 'MyReviews/chartpage.html', context)

def searchpage(request):
    return render(request, 'MyReviews/searchpage.html', context)

def profilepage(request):
    return render(request, 'MyReviews/userprofile.html', context)