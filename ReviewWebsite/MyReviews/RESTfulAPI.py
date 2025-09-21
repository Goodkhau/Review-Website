from rest_framework.generics import ListCreateAPIView
from django.http import JsonResponse
from django.shortcuts import render
from .models import Movie, Review, Genre, User, Person
from .serializers import PersonSerializer, ReviewSerializer, GenreSerializer, MovieSerializer


class CreatePerson(ListCreateAPIView):
    queryset = Person.objects.all()[:5]
    serializer_class = PersonSerializer

class CreateGenre(ListCreateAPIView):
    queryset = Genre.objects.all()[:5]
    serializer_class = GenreSerializer

class CreateReview(ListCreateAPIView):
    queryset = Review.objects.all()[:5]
    serializer_class = ReviewSerializer

class CreateMovie(ListCreateAPIView):
    queryset = Movie.objects.all()[:5]
    serializer_class = MovieSerializer