from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'Home'),
    path('search', views.find_matched_words, name='SearchWords')
]