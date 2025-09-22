from rest_framework import generics
from django.http import JsonResponse
from django.shortcuts import render
from .models import Movie, Review, Genre, User, Person
from .serializers import PersonSerializer, ReviewSerializer, GenreSerializer, MovieSerializer


class CreatePerson(generics.ListCreateAPIView):
    queryset = Person.objects.all()[:5]
    serializer_class = PersonSerializer

class CreateGenre(generics.ListCreateAPIView):
    queryset = Genre.objects.all()[:5]
    serializer_class = GenreSerializer

class CreateReview(generics.ListCreateAPIView):
    queryset = Review.objects.all()[:5]
    serializer_class = ReviewSerializer

class RetrieveUpdateDeleteReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'pk'

class CreateMovie(generics.ListCreateAPIView):
    queryset = Movie.objects.all()[:5]
    serializer_class = MovieSerializer