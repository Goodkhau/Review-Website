from rest_framework import serializers
from .models import Movie, Genre, Person, Review, User


class GetGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'description', 'contributors']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'description']

class GetPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'birth', 'death', 
                  'biography', 'picture', 'contributors']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'birth', 'death', 
                  'biography', 'picture']

class GetMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'poster',
                  'average_score', 'total_score',
                  'number_reviews', 'genre_list', 'release_date', 
                  'runtime', 'date_added', 'modified_at',
                  'director', 'cast', 'crew',
                  'contributors']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'poster', 
                  'genre_list', 'release_date', 
                  'runtime', 'director', 'cast', 
                  'crew', 'contributors']

class GetReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie', 'reviewer', 'created_at', 
                  'modified_at', 'score', 'body']

class PatchReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['score', 'body']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['movie', 'score', 'body']