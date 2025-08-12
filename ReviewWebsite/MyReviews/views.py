from django.shortcuts import render, redirect
from .models import Movie, Review, Genre, User

def homepage(request):
    movie_genres = []
    movies = Movie.objects.all().order_by('-release_date')[:10]
    for movie in movies:
        genres = movie.genre_list.all()
        temp = [movie, genres]
        movie_genres.append(temp)
    reviews = Review.objects.all().order_by('-created_at')[:10]
    context = {'reviews': reviews, 'movie_genres': movie_genres}
    return render(request, 'MyReviews/homepage.html', context)

def genrehome(request):
    context = {}
    return render(request, 'MyReviews/genrehome.html', context)

def genrepage(request):
    genre = Genre.objects.get(id=pk)
    context = {'genre': genre}
    return render(request, 'MyReviews/genrepage.html', context)

def charthome(request):
    movies = Movie.objects.all().order_by('-average_score')[:10]
    context = {'movies': movies}
    return render(request, 'MyReviews/chartpage.html', context)

def chartpage(request):
    start = (pk-1)*10
    end = pk*10
    movies = Movie.objects.all().order_by('-average_score')[start:end]
    context = {'movies': movies}
    return render(request, 'MyReviews/chartpage.html', context)

def searchpage(request):
    context = {}
    return render(request, 'MyReviews/searchpage.html', context)

def profilepage(request):
    context = {}
    return render(request, 'MyReviews/userprofile.html', context)