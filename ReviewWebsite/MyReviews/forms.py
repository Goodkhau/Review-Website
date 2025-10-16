from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Movie, User, Review, Genre, Person

class MovieForm(forms.FORM):
    title = forms.CharField(max_length=100)
    description = forms.TextField(blank=True)
    poster = forms.ImageField(default='fallback.png', blank=True)
    genre_list = forms.ManyToManyField(Genre, related_name='genre_list', blank=True)
    release_date = forms.DateField(blank=True, null=True)
    runtime = forms.IntegerField()
    director = forms.ManyToManyField(Person, related_name='director', blank=True)
    cast = forms.ManyToManyField(Person, related_name='cast', blank=True)
    crew = forms.ManyToManyField(Person, related_name='crew', blank=True)

class ReviewForm(forms.FORM):
    score = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    body = forms.TextField(blank=True)

## class UserForm(forms.FORM):
    ## Add about me