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
    def post():
        return Response()
    def get():
        return Response()

## Post should include review as contributor. If there is no reviewer, a review should not be made.
## Get should be queriable by user and movie.
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
            return Response(status=status.HTTP_404_NOT_FOUND)
        
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