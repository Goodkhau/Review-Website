from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Movie, Review, Genre, User, Person
from .serializers import PersonSerializer, ReviewSerializer, GenreSerializer, MovieSerializer, UserSerializer


## Post should automatically include request.user as contributor. If the user is not authenticated, a movie should not be made.
## Get should return at most 10 movies and options for searching movies by any movie attibute should be possible
class MovieAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        movie = MovieSerializer(data=request.data, partial=True)

        if not movie.is_valid():
            return Response(movie.errors, status=status.HTTP_400_BAD_REQUEST)
        
        movie.save(contributors=[request.user])
        return Response(movie.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        title = request.GET.get("title")
        title = title if title != None else ""

        try:
            scoreGTE = int(request.GET.get("scoreGTE"))
            scoreGTE = scoreGTE if scoreGTE != None else 0
            scoreLTE = int(request.GET.get("scoreLTE"))
            scoreLTE = scoreLTE if scoreLTE != None else 0
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            numGTE = int(request.GET.get("numGTE"))
            numGTE = numGTE if numGTE != None else 0
            numLTE = int(request.GET.get("numLTE"))
            numLTE = numLTE if numLTE != None else 0
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        genre = request.GET.get("genre")
        list = []
        while genre != None:
            g = Genre.objects.get(pk=genre)
            if g is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            list.append(g)
            genre = request.GET.get("genre")

        movies = Movie.objects.all()[:3]
        movies = MovieSerializer(movies, many=True)
        return Response(movies.data, status=status.HTTP_200_OK)

class ReviewAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        review = ReviewSerializer(data=request.data, partial=True)

        if not review.is_valid():
            return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)
        
        review.save(reviewer=request.user)
        return Response(review.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        movie = request.GET.get("movie")
        movie = movie if movie != None else ""
        reviewer = request.GET.get("user")
        reviewer = reviewer if reviewer != None else ""

        reviews = Review.objects.filter(
            Q(movie__title__icontains=movie) &
            Q(reviewer__username__icontains=reviewer)
        )[:5]

        ## If reviews queryset is empty
        if not reviews:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        reviews = ReviewSerializer(reviews, many=True)
        return Response(reviews.data)

## Post automatic add to contributors. Need to be a user to post
## Get queriable by contributor and name
class GenreAPI(APIView):
    def post(self, request):
        return Response()
    def get(self, request):
        return Response()

## Post only one user should be made at a time. Need to be a user to post
## Get only queriable by pk
class UserAPI(APIView):
    def get(self, request):
        return Response()

## Post add user to contrib. Need to be a user to post
## Get queriable by birth death and name
class PersonAPI(APIView):
    def post(self, request):
        return Response()
    def get(self, request):
        return Response()