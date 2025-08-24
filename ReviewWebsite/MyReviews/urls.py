from . import views
from . import userviews
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='home-page'),
    path('movie/<int:pk>/', views.moviepage, name='movie-page'),
    path('genre/', views.genrehome, name='genre-home'),
    path('genre/<int:pk>/', views.genrepage, name='genre-page'),
    path('chart/', views.charthome, name='chart-home'),
    path('chart/<int:pk>/', views.chartpage, name='chart-page'),
    path('search/', views.searchpage, name='search-page'),
    path('profile/<int:pk>/', userviews.profilepage, name='profile-page'),
    path('login/', userviews.loginpage, name='login-page'),
    path('logout/', userviews.logoutrequest, name='logout'),
    path('register/', userviews.registerpage, name='register-page'),
]