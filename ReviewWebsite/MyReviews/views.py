from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Movie, Review, Genre, User, Person

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
    genre = Genre.objects.get(name=pk)
    movies = genre.genre_list.all().order_by('release_date')
    num_movie = movies.count()
    movies = movies[:10]
    context = {'genre': genre, 'movies': movies, 'num_movie': num_movie}
    return render(request, 'MyReviews/genrepage.html', context)

def charthome(request):
    movies = Movie.objects.all().order_by('-average_score')[:10]
    year_str = str(" of All Time")
    context = {'movies': movies, 'year_str': year_str}
    return render(request, 'MyReviews/chartpage.html', context)

def chartpage(request, pk):
    start = (pk-1)*10
    end = pk*10
    movies = Movie.objects.all().order_by('-average_score')[start:end]
    year_str = str(" of All Time")
    context = {'movies': movies, 'year_str': year_str}
    return render(request, 'MyReviews/chartpage.html', context)

def chartpage_yr(request, yr, pk):
    start = (pk-1)*10
    end = pk*10
    movies = Movie.objects.filter(Q(release_date__year=yr)).order_by('-average_score')[start:end]
    year_str = " of " + str(yr)
    context = {'movies': movies, 'year_str': year_str}
    return render(request, 'MyReviews/chartpage.html', context)

def chartpage_range(request, yr1, yr2, pk):
    start = (pk-1)*10
    end = pk*10
    movies = Movie.objects.filter(
        Q(release_date__year__gte=yr1),
        Q(release_date__year__lte=yr2)
    ).order_by('-average_score')[start:end]
    year_str = " of " + str(yr1) + " - " + str(yr2)
    context = {"movies": movies, "year_str": year_str}
    return render(request, 'MyReviews/chartpage.html', context)

def searchpage(request):
    q = request.GET.get('search_query') if request.GET.get('search_query') != None else ''
    movies = Movie.objects.filter (
        Q(title__icontains=q)
    )[:5]
    people = Person.objects.filter (
        Q(name__icontains=q)
    )[:5]
    users = User.objects.filter (
        Q(username__icontains=q)
    )[:5]
    context = {'movies': movies, 'people': people, 'users': users}
    return render(request, 'MyReviews/searchpage.html', context)