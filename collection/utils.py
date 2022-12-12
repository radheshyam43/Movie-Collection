from collections import Counter


def get_favourite_geners(collections):
    '''
    Return 3 or less most frequent genre in all collections
    arguments: List of collection objects

    return: comma separated list of at max 3 genres
    '''
    movie_set = set()
    for collection in collections:
        for movie in collection.movies.all():
            movie_set.add(movie)

    genres_list = []
    for movie in movie_set:
        genres_list.extend(movie.genres.split(','))
    most_common_genres = Counter(genres_list).most_common(3)
    return list(map(lambda x: x[0], most_common_genres))
