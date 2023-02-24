def filter_movies(movies, filters: dict):
    if filters['search']:
        movies = movies.filter(title__icontains=filters['search'])

    if filters['release_date']:
        movies = movies.filter(release_date__gte=filters['release_date'])
    return  movies