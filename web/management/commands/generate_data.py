import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import Movie, User, MovieGenre


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()
        user = User.objects.first()
        genres = MovieGenre.objects.filter(user=user)

        movies = []

        for day_index in range(10):
            current_date -= timedelta(days=1)

            for movie_index in range(randint(5, 10)):
                release_date = current_date + timedelta(hours=randint(0, 10))

                movies.append(Movie(
                    title=f'generated {day_index}-{movie_index}',
                    release_date=release_date,
                    user=user
                ))

        saved_movies = Movie.objects.bulk_create(movies)
        movies_genres = []
        for movie in saved_movies:
            count_of_genres = randint(0, len(genres))
            for genre_index in range(count_of_genres):
                movies_genres.append(
                    Movie.genres.through(movie_id=movie.id, moviegenre_id=genres[genre_index].id)
                )
        Movie.genres.through.objects.bulk_create(movies_genres)