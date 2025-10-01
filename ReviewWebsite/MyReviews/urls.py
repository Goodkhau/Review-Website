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

    path('profile/<str:pk>/', userviews.profilepage, name='profile-page'),
    path('login/', userviews.loginpage, name='login-page'),
    path('logout/', userviews.logoutrequest, name='logout'),
    path('register/', userviews.registerpage, name='register-page'),
    path('activate/<str:uidb64>/<str:token>/', userviews.activate, name='activate'),

    path('api/v1/review/', RESTfulAPI.ReviewAPI.as_view(), name='api-review'),
]