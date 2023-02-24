from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, movies_edit_view, genres_view, \
    genre_delete_view, movie_delete_view

urlpatterns = [
    path("", main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("movies/add/", movies_edit_view, name="movies_add"),
    path("movies/<int:id>/", movies_edit_view, name="movies_edit"),
    path("genres/", genres_view, name="genres"),
    path("genres/<int:id>/delete/", genre_delete_view, name="genre_delete"),
    path("movies/<int:id>/delete/", movie_delete_view, name="movie_delete"),
]