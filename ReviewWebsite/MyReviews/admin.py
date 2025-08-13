from django.contrib import admin

# Register your models here.
from .models import Genre, Movie, User, Review, Person

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Person)