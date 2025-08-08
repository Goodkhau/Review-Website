from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    average_score = models.DecimalField(max_digits=2, decimal_places=2, null=True)
    genre_list = models.ManyToManyField(Genre, related_name='genre_list', blank=True)
    release_date = models.DateField()
    runtime = models.DurationField()

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True)
    # verification_token
    # verification_expire
    # verification_date
    # reset_expire
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["email"]

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    score = models.IntegerField()
    body = models.TextField(blank=True)