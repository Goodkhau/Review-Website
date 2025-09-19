from rest_framework import serializers
from .models import Movie, Genre, Person, Review, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'picture']

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
    genre_list = GenreSerializer(many=True)
    director = PersonSerializer()
    cast = PersonSerializer(many=True)
    crew = PersonSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'description', 
                  'poster', 'average_score', 'total_score', 
                  'number_reviews', 'genre_list', 'release_date', 
                  'runtime', 'date_added', 'director', 
                  'cast', 'crew']
        
class ReviewSerializer(serializers.Serializer):
    movie = MovieSerializer()
    reviewer = UserSerializer()
    class Meta:
        model = Review
        fields = ['movie', 'reviewer', 'created_at', 
                  'modified_at', 'score', 'body']