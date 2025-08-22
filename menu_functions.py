import random
import matplotlib.pyplot as plt
import requests

from api_data_fetcher import get_movie_data_from_api, APIError
from movie_storage import movie_storage_sql as storage


WHITE = "\033[0m"
RED = "\033[91m"
BLUE = "\033[94m"
GREEN = "\033[92m"


def red_text(text: str) -> str:
    """
    Wraps the given text in red ANSI color codes for console output.
    :param text: The text to format.
    :return: The formatted red text.
    """
    return f'{RED}{text}{WHITE}'


def blue_text(text: str) -> str:
    """
    Wraps the given text in blue ANSI color codes for console output.
    :param text: The text to format.
    :return: The formatted blue text.
    """
    return f'{BLUE}{text}{WHITE}'


def green_text(text: str) -> str:
    """
    Wraps the given text in green ANSI color codes for console output.
    :param text: The text to format.
    :return: The formatted green text.
    """
    return f'{GREEN}{text}{WHITE}'


def green_input(text: str) -> str:
    """
    Prompts the user for input with green ANSI text formatting.
    :param text: The input prompt to display.
    :return: The user-entered string.
    """
    input_string = input(text + GREEN)
    print(WHITE, end="")
    return input_string


def print_movie_list():
    """
    Prints all stored movies as a formatted list.
    :return: None
    """
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total\n")

    for movie in movies:
        print(get_movie_text(movie))


def add_movie():
    """
    Prompts the user for a movie name, fetches data from the API,
    and adds the movie to the database.
    :return: None
    """
    new_movie_name = green_input("Enter new movie name: ")

    try:
        movie_data = get_movie_data_from_api(new_movie_name)
        storage.add_movie(movie_data)
    except requests.exceptions.ConnectionError:
        print(red_text("Connection error, try again later."))
    except APIError as e:
        print(red_text(str(e)))


def delete_movie():
    """
    Prompts the user for a movie name and deletes it from the database if it exists.
    :return: None
    """
    movies = storage.list_movies()
    movie_to_delete = green_input("Enter movie name to delete: ")

    if movies.get(movie_to_delete):
        storage.delete_movie(movie_to_delete)
    else:
        print(red_text(f"That movie doesn't exist."))


def print_stats():
    """
    Prints statistics about all stored movies, including average and median rating,
    as well as the best and worst movies.
    :return: None
    """
    movies = storage.list_movies()
    ratings = [movies[m]["rating"] for m in movies]

    average = sum(ratings) / len(movies)
    print(f"Average rating: \t{round(average, 2)}")

    ratings.sort()
    middle = len(movies) / 2
    if len(movies) % 2 == 0:
        median = (ratings[int(middle)] + ratings[int(middle) - 1]) / 2
    else:
        median = ratings[int(middle)]

    print(f"Median rating: \t\t{round(median, 2)}\n")

    sorted_names = sorted(movies.keys(), key=lambda key: movies[key]["rating"])
    best_count = ratings.count(max(ratings))
    worst_count = ratings.count(min(ratings))

    if best_count > 1:
        print("Best movies:")
        for movie in sorted_names[-best_count:]:
            print(get_movie_text(movie))
    else:
        best_movie = max(movies, key=lambda key: movies[key]["rating"])
        print(f"Best movie: \t{get_movie_text(best_movie)}")

    print()

    if worst_count > 1:
        print("Worst movies:")
        for movie in sorted_names[:worst_count]:
            print(get_movie_text(movie))
    else:
        worst_movie = min(movies, key=lambda key: movies[key]["rating"])
        print(f"Worst movie: \t{get_movie_text(worst_movie)}")


def random_movie():
    """
    Selects and prints a random movie from the database.
    :return: None
    """
    movies = storage.list_movies()
    movie_names = list(movies.keys())
    random_index = random.randrange(0, len(movie_names) - 1)
    random_movie_name = movie_names[random_index]

    print(
        f"Your movie for tonight: {random_movie_name} "
        f"({movies[random_movie_name]['year']}), "
        f"it's rated {movies[random_movie_name]['rating']}"
    )


def search_movie():
    """
    Prompts the user for a search string and searches movies by name.
    Performs exact and fuzzy matching.
    :return: None
    """
    movies = storage.list_movies()
    search_input = green_input("Enter part of movie name: ")

    search_results = [m for m in movies if search_input.lower() in m.lower()]
    fuzzy_search = False

    if not search_results:
        for movie in movies:
            if get_edit_distance(search_input, movie) < 3:
                search_results.append(movie)
                fuzzy_search = True
            else:
                for word in movie.split():
                    if get_edit_distance(search_input, word) < 3:
                        search_results.append(movie)
                        fuzzy_search = True
                        break

    if fuzzy_search:
        print(f"The movie '{search_input}' doesn't exist. Did you mean:")
    else:
        print(f"{len(search_results)} movies found.")

    print()
    for movie in search_results:
        print(get_movie_text(movie))


def print_sorted_list_rating():
    """
    Prints all movies sorted by rating in descending order.
    :return: None
    """
    movies = storage.list_movies()
    sorted_names = sorted(movies.keys(), key=lambda key: movies[key]["rating"])

    print()
    for movie in sorted_names[::-1]:
        print(get_movie_text(movie))


def print_sorted_list_release(min_rating: float = 0, min_year: int = 0, max_year: int = 3000):
    """
    Prints all movies sorted by release year, filtered by rating and year range.
    :param min_rating: Minimum displayed rating (default 0).
    :param min_year: Minimum release year (default 0).
    :param max_year: Maximum release year (default 3000).
    :return: None
    """
    movies = storage.list_movies()
    sorted_names = sorted(movies.keys(), key=lambda key: movies[key]["year"])

    while True:
        order_input = input("Begin with first movie? [Y/N] ")
        if order_input in ["Y", "N", "y", "n"]:
            break
        else:
            print(red_text("Invalid input. Please try again."))

    if order_input.lower() == "n":
        sorted_names.reverse()

    print()
    for movie in sorted_names:
        if min_year <= movies[movie]["year"] <= max_year and movies[movie]["rating"] >= min_rating:
            print(get_movie_text(movie))


def get_movie_text(title: str) -> str:
    """
    Returns a formatted string with movie title, year, and rating.
    :param title: The movie title.
    :return: A string with movie details.
    """
    year, rating, poster = storage.get_movie(title)
    return f"{title} ({year}), {rating}"


def filter_movies():
    """
    Prompts the user for filtering criteria (rating, min/max year)
    and prints movies that match.
    :return: None
    """
    minimum_rating = 0
    while True:
        try:
            minimum_rating_input = input("Enter minimum rating (leave blank for no minimum rating):")
            if minimum_rating_input == "":
                break
            minimum_rating = float(minimum_rating_input)
            if is_valid_rating(minimum_rating_input):
                break
            else:
                raise ValueError()
        except ValueError:
            print(red_text("Invalid input. Please try again."))

    min_year = 0
    while True:
        try:
            min_year_input = input("Enter minimum release year (leave blank for no minimum):")
            if min_year_input == "":
                break
            min_year = int(min_year_input)
            break
        except ValueError:
            print(red_text("Invalid input. Please try again."))

    max_year = 3000
    while True:
        try:
            max_year_input = input("Enter maximum release year (leave blank for no maximum):")
            if max_year_input == "":
                break
            max_year = int(max_year_input)
            if max_year > min_year:
                break
            else:
                raise ValueError
        except ValueError:
            print(red_text("Invalid input. Please try again."))

    print_sorted_list_release(minimum_rating, min_year, max_year)


def generate_website():
    """
    Generates an HTML website from stored movies using a template.
    :return: None
    """
    with open("html_data/index_template.html", "r") as template_file:
        template_content = template_file.read()

    movies = storage.list_movies()
    movies_html_grid = "".join(get_html_movie(m) for m in movies)

    website_content = template_content.replace("__TEMPLATE_TITLE__", "Movie Database")
    website_content = website_content.replace("__TEMPLATE_MOVIE_GRID__", movies_html_grid)

    with open("html_data/index.html", "w") as index_file:
        index_file.write(website_content)

    print("The website has been successfully generated!")


def get_html_movie(movie_title: str) -> str:
    """
    Returns an HTML snippet for a movie including poster, title, and year.
    :param movie_title: The title of the movie.
    :return: HTML string representing the movie.
    """
    html_string = """
    <li>
        <div class="movie">
            <img class="movie-poster"
                 src="_POSTER_URL_"/>
            <div class="movie-title">_MOVIE_TITLE</div>
            <div class="movie-year">_MOVIE_YEAR_</div>
        </div>
    </li>
    """
    year, rating, poster = storage.get_movie(movie_title)

    html_string = html_string.replace("_POSTER_URL_", poster)
    html_string = html_string.replace("_MOVIE_TITLE", movie_title)
    html_string = html_string.replace("_MOVIE_YEAR_", str(year))

    return html_string


def create_histogram():
    """
    Creates a histogram of movie ratings and saves it as a PNG file.
    :return: None
    """
    movies = storage.list_movies()
    rating_counts = {}

    for i in range(1, 11):
        rating_counts[i] = 0

    for movie in movies:
        rating = movies[movie]["rating"]
        rating_counts[round(rating)] += 1

    counts = list(rating_counts.values())
    ratings = list(rating_counts.keys())

    plt.bar(ratings, counts, color = "green", width=0.5)
    plt.xlabel("Movie Rating")
    plt.xticks(ratings, ratings, rotation=0)
    plt.ylabel("Count")
    plt.title("Movie Ratings")


    name_input = green_input("Enter the name of the file: ")
    plt.savefig(f"{name_input}.png")
    print(f"The file was saved under '{name_input}.png'.")


def is_valid_rating(number_string: str) -> bool:
    """
    Validates whether a given string represents a valid rating between 0 and 10.
    :param number_string: The string to validate.
    :return: True if valid, False otherwise.
    """
    return number_string.replace(".", "", 1).isdigit() and 0 <= float(number_string) <= 10


def get_edit_distance(word: str, compare_to: str) -> int:
    """
    Calculates the edit distance (difference) between two strings.
    :param word: The word to compare.
    :param compare_to: The reference word.
    :return: The edit distance as an integer.
    """
    distance = 0
    word = word.lower()
    compare_to = compare_to.lower()
    word_list = list(word)

    for i, char in enumerate(compare_to):
        if word_list[i:] == list(compare_to[i:]):
            break
        elif i < len(word_list) and word_list[i] == char:
            continue

        distance += 1
        if i > len(word_list) - 1:
            word_list.append(compare_to[i])
        elif i < len(word_list) - 1 and word_list[i + 1] == char:
            del word_list[i]
        elif i < len(compare_to) - 1 and word_list[i] == compare_to[i + 1]:
            word_list.insert(i, compare_to[i])
        else:
            word_list[i] = char

    if len(word_list) > len(compare_to):
        distance += len(word_list) - len(compare_to)

    return distance


def quit_program():
    """
    Exits the program.
    :return: None
    """
    print("Bye!")
    quit()
