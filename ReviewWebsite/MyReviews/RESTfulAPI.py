from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
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
    def post(self, request, pk):
        review = ReviewSerializer(data=request.data)
        review.reviewer = request.user.pk

        if not review.is_valid:
            return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)
        
        review.save()
        return Response(review.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, pk):
        reviews = Review.objects.all()[:5]
        reviews = ReviewSerializer(reviews, many=True)
        return Response(reviews.data)

## Post automatic add to contributors
## Get queriable by contributor and name
class GenreAPI(APIView):
    def post(self, request):
        return Response()
    def get(self, request):
        return Response()

## Post only one user should be made at a time
## Get only queriable by pk
class UserAPI(APIView):
    def get(self, request):
        return Response()

## Post add user to contrib
## Get queriable by birth death and name
class PersonAPI(APIView):
    def post(self, request):
        return Response()
    def get(self, request):
        return Response()