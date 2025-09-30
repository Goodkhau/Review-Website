from rest_framework import serializers
from .models import Movie, Genre, Person, Review, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'description']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'birth', 'death', 
                  'biography', 'picture']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'poster', 
                  'genre_list', 'release_date', 
                  'runtime', 'director', 'cast', 
                  'crew']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['movie', 'score', 'body']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'picture']