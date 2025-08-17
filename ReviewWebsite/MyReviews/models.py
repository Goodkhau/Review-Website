from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    birth = models.DateField(blank=True)
    death = models.DateField(blank=True)
    biography = models.TextField(blank=True)

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    poster = models.ImageField(default='fallback.png', blank=True)
    total_score = models.IntegerField(default=0)
    number_reviews = models.IntegerField(default=0)
    genre_list = models.ManyToManyField(Genre, blank=True)
    release_date = models.DateField()
    runtime = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    director = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True, blank=True)
    cast = models.ManyToManyField(Person, related_name='cast', blank=True)
    crew = models.ManyToManyField(Person, related_name='crew', blank=True)

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # verification_token
    # verification_expire
    # verification_date
    # reset_expire
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["email"]

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField()
    body = models.TextField(blank=True)