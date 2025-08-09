from django.shortcuts import render, redirect
from .models import Movie, Review

def home(request):
    movies = Movie.objects.all().order_by('-release_date')[:10]
    reviews = Review.objects.all().order_by('-created_at')[:10]
    context = {'movies': movies, 'reviews': reviews}
    return render(request, 'MyReviews/homepage.html', context)