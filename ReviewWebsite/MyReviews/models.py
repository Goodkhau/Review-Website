from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You did not enter an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='profilefallback.png', blank=True)

    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["email"]

class Genre(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(blank=True)
    contributors = models.ManyToManyField(User, related_name='genre_contrib', blank=True)

class Person(models.Model):
    name = models.CharField(max_length=40)
    birth = models.DateField(blank=True, null=True)
    death = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True)
    picture = models.ImageField(default='profilefallback.png', blank=True)
    contributors = models.ManyToManyField(User, related_name='person_contrib', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    poster = models.ImageField(default='fallback.png', blank=True)
    average_score = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    total_score = models.IntegerField(default=0)
    number_reviews = models.IntegerField(default=0)
    genre_list = models.ManyToManyField(Genre, related_name='genre_list', blank=True)
    release_date = models.DateField(blank=True, null=True)
    runtime = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    director = models.ManyToManyField(Person, related_name='director', blank=True)
    cast = models.ManyToManyField(Person, related_name='cast', blank=True)
    crew = models.ManyToManyField(Person, related_name='crew', blank=True)
    contributors = models.ManyToManyField(User, related_name='movie_contrib', blank=True)

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.SET_NULL, null=True)
    reviewer = models.ForeignKey(User, related_name='reviewer', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField()
    body = models.TextField(blank=True)