from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Movie, User, Review, Genre, Person

class MovieForm(forms.Form):
    class Meta:
        model = Movie
    
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description (optional)")
    poster = forms.ImageField(required=False)
    genre_list = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False)
    release_date = forms.DateField(required=False)
    runtime = forms.IntegerField(required=False)
    director = forms.ModelMultipleChoiceField(queryset=Person.objects.all(), required=False)
    cast = forms.ModelMultipleChoiceField(queryset=Person.objects.all(), required=False)
    crew = forms.ModelMultipleChoiceField(queryset=Person.objects.all(), required=False)

class ReviewForm(forms.Form):
    class Meta:
        model = Review
    
    movie = forms.ModelChoiceField(queryset=Movie.objects.all()[:5], empty_label="Select a film")
    score = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    body = forms.CharField(widget=forms.Textarea, required=False, label="Body (optional)")

## class UserForm(forms.FORM):
    ## Add about me