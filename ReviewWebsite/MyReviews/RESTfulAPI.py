from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Movie, Review, Genre, Person
from .serializers import GetPersonSerializer, PersonSerializer, GetReviewSerializer, PatchReviewSerializer, ReviewSerializer, GetGenreSerializer, GenreSerializer, GetMovieSerializer, MovieSerializer
import datetime
from datetime import date
import math


## Create a owner column to police delete function.
## Update contributors on patch.

class SingleMovieAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        movie = GetMovieSerializer(movie)
        return Response(data=movie.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        movie.genre_list.clear()
        movie.director.clear()
        movie.cast.clear()
        movie.crew.clear()
        movie.contributors.clear()
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        movie = MovieSerializer(movie, data=request.data, partial=True)
        if not movie.is_valid():
            return Response(movie.errors, status=status.HTTP_400_BAD_REQUEST)

        movie.save()
        return Response(movie.data, status=status.HTTP_201_CREATED)

class MovieAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        movie = MovieSerializer(data=request.data, partial=True)

        if not movie.is_valid():
            return Response(movie.errors, status=status.HTTP_400_BAD_REQUEST)
        
        movie.save(contributors=[request.user])
        return Response(movie.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        ## Title
        title = request.GET.get("title")
        title = title if title != None else ""

        ## Average Score Range
        try:
            scoreGTE = request.GET.get("scoreGTE")
            scoreGTE = float(scoreGTE) if scoreGTE != None else 0
            scoreLTE = request.GET.get("scoreLTE")
            scoreLTE = float(scoreLTE) if scoreLTE != None else 10
            scoreNone = request.GET.get("scoreNone")
            if scoreNone == None:
                scoreNoneQ = Q(average_score=None)
            else:
                scoreNoneQ = Q(average_score=-404)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        ## Number of Reviews Range
        try:
            numGTE = request.GET.get("numGTE")
            numGTE = math.ceil(float(numGTE)) if numGTE != None else 0
            numLTE = request.GET.get("numLTE")
            numLTE = math.floor(float(numLTE)) if numLTE != None else 9999999
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        ## Genres
        genre = request.GET.getlist("genre")
        list = []
        for g in genre:
            try:
                temp = Genre.objects.get(pk=g)
            except:
                continue
            list.append(temp)
        genreQuery = Q()
        if len(list) != 0:
            genreQuery = Q(genre_list__in=list)
        
        ## Date Range
        try:
            dateGTE = request.GET.get("dateGTE")
            dateGTE = dateGTE.split('-') if dateGTE != None else None
            dateGTE = date(int(dateGTE[0]), int(dateGTE[1]), int(dateGTE[2])) if dateGTE != None else date(datetime.MINYEAR,1,1)
            dateLTE = request.GET.get("dateLTE")
            dateLTE = dateLTE.split('-') if dateLTE != None else None
            dateLTE = date(int(dateLTE[0]), int(dateLTE[1]), int(dateLTE[2])) if dateLTE != None else date.today()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        ## Runtime Range
        try:
            runtimeGTE = request.GET.get("runtimeGTE")
            runtimeGTE = int(runtimeGTE) if runtimeGTE != None else 0
            runtimeLTE = request.GET.get("runtimeLTE")
            runtimeLTE = int(runtimeLTE) if runtimeLTE != None else 999999
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        movies = Movie.objects.filter(
            Q(title__icontains=title) &
             (scoreNoneQ | 
              (Q(average_score__gte=scoreGTE) &
               Q(average_score__lte=scoreLTE)
               )
              ) &
            Q(number_reviews__gte=numGTE) &
            Q(number_reviews__lte=numLTE) &
            genreQuery &
            Q(release_date__gte=dateGTE) &
            Q(release_date__lte=dateLTE) &
            Q(runtime__gte=runtimeGTE) &
            Q(runtime__lte=runtimeLTE)
        ).order_by("-date_added")[:5]

        if len(movies) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        movies = GetMovieSerializer(movies, many=True)
        return Response(movies.data, status=status.HTTP_200_OK)

class SingleReviewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            review = Review.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        review = GetReviewSerializer(review)
        return Response(review.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if review.movie is not None:
            movie = review.movie
            movie.total_score -= review.score
            movie.number_reviews -= 1
            movie.average_score = movie.total_score/movie.number_reviews if movie.number_review > 0 else None
        
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            review = Review.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        movie = review.movie
        
        review_seralized = PatchReviewSerializer(review, data=request.data, partial=True)
        if not review_seralized.is_valid():
            return Response(review_seralized.errors, status=status.HTTP_400_BAD_REQUEST)

        if movie is not None:
            movie.total_score -= review.score
            movie.total_score += review_seralized.validated_data["score"]
            movie.average_score = movie.total_score/movie.number_reviews
            movie.save()
        
        review_seralized.save()
        return Response(review_seralized.data, status=status.HTTP_201_CREATED)

class ReviewAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        has_review = request.user.reviewer.get(movie=request.data["movie"])
        if has_review is not None:
            return Response(status=status.HTTP_200_OK)
        
        review = ReviewSerializer(data=request.data, partial=True)

        if not review.is_valid():
            return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)

        movie = review.validated_data["movie"]
        movie.total_score += review.validated_data["score"]
        movie.number_reviews += 1
        movie.average_score = movie.total_score if movie.average_score is None else movie.total_score/movie.number_reviews
        
        movie.save()
        review.save(reviewer=request.user)
        return Response(review.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        movie = request.GET.get("movie")
        movie = movie if movie != None else ""
        reviewer = request.GET.get("user")
        reviewer = reviewer if reviewer != None else ""

        reviews = Review.objects.filter(
            Q(movie__title__icontains=movie) &
            Q(reviewer__username__icontains=reviewer)
        )[:5]

        ## If reviews queryset is empty
        if not reviews:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        reviews = GetReviewSerializer(reviews, many=True)
        return Response(reviews.data, status=status.HTTP_200_OK)

class SingleGenreAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            genre = Genre.objects.get(name=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        genre = GetGenreSerializer(genre)
        return Response(genre.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            genre = Genre.objects.get(name=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        genre.genre_list.clear()
        genre.contributors.clear()
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        try:
            genre = Genre.objects.get(name=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        genre = GenreSerializer(genre, data=request.data, partial=True)
        if not genre.is_valid():
            return Response(genre.errors, status=status.HTTP_400_BAD_REQUEST)
        
        genre.save()
        return Response(genre.data, status=status.HTTP_200_OK)

class GenreAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        genre = GenreSerializer(data=request.data, partial=True)

        if not genre.is_valid():
            return Response(genre.errors, status=status.HTTP_400_BAD_REQUEST)
        
        genre.save(contributors=[request.user])
        return Response(genre.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        name = request.GET.get("name")
        name = name if name is not None else ""
        genres = Genre.objects.filter(
            Q(name__icontains=name)
        )[:5]
        genres = GetGenreSerializer(genres, many=True)
        return Response(genres.data, status=status.HTTP_200_OK)

## Create patch and update get
class SinglePersonAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            person = Person.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        person = GetPersonSerializer(person)
        return Response(person.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            person = Person.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        person.contributors.clear()
        person.director.clear()
        person.cast.clear()
        person.crew.clear()
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        try:
            person = Person.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        person = PersonSerializer(person, data=request.data, partial=True)
        if not person.is_valid():
            return Response(person.errors, status=status.HTTP_400_BAD_REQUEST)
        
        person.save()
        return Response(person.data, status=status.HTTP_200_OK)

class PersonAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        person = PersonSerializer(data=request.data, partial=True)
        if not person.is_valid():
            return Response(person.errors, status=status.HTTP_400_BAD_REQUEST)
        
        person.save(contributors=[request.user])
        return Response(person.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        name = request.GET.get("name")
        name = name if name is not None else ""
        people = Person.objects.filter(
            Q(name__icontains=name)
        )[:5]
        people = GetPersonSerializer(people, many=True)
        return Response(people.data, status=status.HTTP_200_OK)