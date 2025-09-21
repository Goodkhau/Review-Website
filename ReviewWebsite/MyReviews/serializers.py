from rest_framework import serializers
from .models import Movie, Genre, Person, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_id', 'name', 'description']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'birth', 'death', 
                  'biography', 'picture']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'description', 
                  'poster', 'average_score', 'total_score', 
                  'number_reviews', 'genre_list', 'release_date', 
                  'runtime', 'date_added', 'director', 
                  'cast', 'crew']
        
class ReviewSerializer(serializers.Serializer):
    class Meta:
        model = Review
        fields = ('movie', 'reviewer', 'created_at', 'modified_at', 'score', 'body')