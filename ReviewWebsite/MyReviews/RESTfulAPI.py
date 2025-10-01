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