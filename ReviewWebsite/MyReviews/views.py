from django.shortcuts import render, redirect
from .models import Movie, Review, Genre, User

def homepage(request):
    movie_genres = []
    movies = Movie.objects.all().order_by('-release_date')[:10]
    for movie in movies:
        genres = movie.genre_list.all().order_by('name')
        rating = None if movie.number_reviews == 0 else movie.total_score/movie.number_reviews
        temp = [movie, genres, rating]
        movie_genres.append(temp)
    
    review_movies = []
    reviews = Review.objects.all().order_by('-created_at')[:10]
    for review in reviews:
        movie = review.movie
        temp = [review, movie]
        review_movies.append(temp)
    
    context = {'review_movies': review_movies, 'movie_genres': movie_genres}
    return render(request, 'MyReviews/homepage.html', context)

def moviepage(request, pk):
    movie = Movie.objects.get(movie_id=pk)
    genres = movie.genre_list.all().order_by('name')
    rating = None if movie.number_reviews == 0 else movie.total_score/movie.number_reviews
    context = {'movie': movie, 'genres': genres, 'rating': rating}
    return render(request, 'MyReviews/moviepage.html', context)

def genrehome(request):
    context = {}
    return render(request, 'MyReviews/genrehome.html', context)

def genrepage(request, pk):
    genre = Genre.objects.get(genre_id=pk)
    movies = genre.movie_set.all()
    num_movie = movies.count()
    context = {'genre': genre, 'movies': movies, 'num_movie': num_movie}
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