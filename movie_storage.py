import json
import os


def get_movies():
    """
    The function loads the information from the JSON
    file and returns the data.
    """
    if not os.path.exists('movie_data.json'):
        return {}

    with open('movie_data.json', 'r') as file:
        movies = json.load(file)

    return movies


def save_movies(movies):
    """
    Gets the movie dictionary as an argument and saves it to the JSON file.
    """
    with open("movie_data.json", "w") as file:
        json.dump(movies, file)


def add_movie(title, year, rating):
    """
    Adds a movie to the movie database.
    """
    movies = get_movies()

    movies[title] = {
        "year": year,
        "rating": rating
    }

    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movi database.
    """
    movies = get_movies()

    del movies[title]

    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    """
    movies = get_movies()

    movies[title]["rating"] = rating

    save_movies(movies)
