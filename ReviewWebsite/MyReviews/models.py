from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You did not enter an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
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
    # verification_token
    # verification_expire
    # verification_date
    # reset_expire

    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    
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