from . import views
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='home-page'),
    path('genre/', views.genrehome, name='genre-home'),
    path('genre/<int:pk>/', views.genrepage, name='genre-page'),
    path('chart/', views.charthome, name='chart-home'),
    path('chart/<int:pk>/', views.chartpage, name='chart-page'),
    path('search/<str:pk>', views.searchpage, name='search-page'),
    path('profile/<int:pk>', views.profilepage, name='profile-page'),
]