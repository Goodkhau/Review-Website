from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from .models import Movie, Review, Genre, User, Person
from .serializers import PersonSerializer, ReviewSerializer, GenreSerializer, MovieSerializer, UserSerializer


class CreatePerson(generics.ListCreateAPIView):
    queryset = Person.objects.all()[:5]
    serializer_class = PersonSerializer

class RetrieveUpdateDeletePerson(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'pk'

class CreateGenre(generics.ListCreateAPIView):
    queryset = Genre.objects.all()[:5]
    serializer_class = GenreSerializer

class RetrieveUpdateDeleteGenre(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'pk'

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

class RetrieveUpdateDeleteMovie(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'pk'

class RetrieveUpdateDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'