from . import views
from . import userviews
from . import RESTfulAPI
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='home-page'),
    path('movie/<int:pk>/', views.moviepage, name='movie-page'),
    path('genre/', views.genrehome, name='genre-home'),
    path('genre/<str:pk>/', views.genrepage, name='genre-page'),
    path('chart/', views.charthome, name='chart-home'),
    path('chart/<int:pk>/', views.chartpage, name='chart-page'),
    path('chart/<int:yr>/<int:pk>/', views.chartpage_yr, name='chart-page'),
    path('chart/<int:yr1>-<int:yr2>/<int:pk>/', views.chartpage_range, name='chart-page'),
    path('search/', views.searchpage, name='search-page'),

    path('profile/<int:pk>/', userviews.profilepage, name='profile-page'),
    path('login/', userviews.loginpage, name='login-page'),
    path('logout/', userviews.logoutrequest, name='logout'),
    path('register/', userviews.registerpage, name='register-page'),
    path('activate/<str:uidb64>/<str:token>/', userviews.activate, name='activate'),

    path('api/v1/person/', RESTfulAPI.CreatePerson.as_view(), name='api-create-person'),
    path('api/v1/person/<int:pk>/', RESTfulAPI.RetrieveUpdateDeletePerson.as_view(), name='api-RUD-person'),
    path('api/v1/review/', RESTfulAPI.CreateReview.as_view(), name='api-create-review'),
    path('api/v1/review/<int:pk>/', RESTfulAPI.RetrieveUpdateDeleteReview.as_view(), name='api-RUD-review'),
    path('api/v1/genre/', RESTfulAPI.CreateGenre.as_view(), name='api-create-genre'),
    path('api/v1/genre/<int:pk>/', RESTfulAPI.RetrieveUpdateDeleteGenre.as_view(), name='api-RUD-genre'),
    path('api/v1/movie/', RESTfulAPI.CreateMovie.as_view(), name='api-create-movie'),
    path('api/v1/movie/<int:pk>/', RESTfulAPI.RetrieveUpdateDeleteMovie.as_view(), name='api-RUD-movie'),
    path('api/v1/user/<int:pk>/', RESTfulAPI.RetrieveUpdateDeleteUser.as_view(), name='api-RUD-user'),
]