from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from .models import Movie, Review, Genre, User, Person
from .serializers import PersonSerializer, ReviewSerializer, GenreSerializer, MovieSerializer, UserSerializer


class PersonAPI(APIView):
    def post(self, request):
        return Response()
    def get(self, request):
        return Response()

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

class ReviewAPI(APIView):
    def post(self, request):
        review = ReviewSerializer(data=request.data)
        review.reviewer = request.user.pk

        if not review.is_valid:
            return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)
        
        review.save()
        return Response(review.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        reviews = Review.objects.all()[:5]
        reviews = ReviewSerializer(reviews, many=True)
        return Response(reviews.data)

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