import random
import matplotlib.pyplot as plt
import requests

import movie_storage_sql as storage

API_Key = "b20d4c97"

WHITE = "\033[0m"
RED = "\033[91m"
BLUE = "\033[94m"
GREEN = "\033[92m"


def red_text(text):
    """
    :return: red text (for console)
    """
    return f'{RED}{text}{WHITE}'


def blue_text(text):
    """
    :return: blue text (for console)
    """
    return f'{BLUE}{text}{WHITE}'


def green_text(text):
    """
    :return: green text (for console)
    """
    return f'{GREEN}{text}{WHITE}'


def green_input(text):
    """
    prints an input line with green input text (for console)
    :param text: input text
    :return: the input
    """
    input_string = input(text + GREEN)
    print(WHITE, end="")
    return input_string

def get_movie_data_from_api(title: str):
    url = f"http://www.omdbapi.com/?apikey={API_Key}&t={title}"

    response = requests.get(url)

    response_data = response.json()

    if response_data.get("Error"):
        error_message = response_data["Error"]
        raise Exception(error_message)

    movie_data = {"title": response_data["Title"],
                  "year": response_data["Year"],
                  "rating": response_data["imdbRating"],
                  "posterURL": response_data["Poster"]}

    return movie_data

def print_title(title):
    print(blue_text("-" * 15 + f" {title} " + "-" * 15))


def menu():
    """
    prints the menu options
    :return: None
    """
    print()
    print(blue_text("Menu:"))

    for index, option in MENU_OPTIONS.items():
        print(blue_text(f"{index}. {option[1]}"))


    while True:
        try:
            print()
            choice_string = int(green_input(f"Enter choice (0-{len(MENU_OPTIONS)-1}): "))
            # check if the input is between 1 and 10
            if MENU_OPTIONS.get(choice_string):
                function = MENU_OPTIONS.get(choice_string)[0]
                function()
                input("\nPress enter to continue")
                break
            else:
                raise ValueError()
        except ValueError:
            print(red_text("Invalid input, try again."))




def print_movie_list():
    """
    prints the movies in a list
    """
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total\n")

    for movie in movies:
        print(get_movie_text(movie))


def add_movie():
    """
    Gets a movie and a rating as input and adds it to the movie dictionary
    :return: None
    """
    new_movie_name = green_input("Enter new movie name: ")

    try:
        movie_data = get_movie_data_from_api(new_movie_name)

        storage.add_movie(movie_data)

    except requests.exceptions.ConnectionError:
        print(red_text("Connection error, try again later."))
    except Exception as e:
        print(red_text(e))



def delete_movie():
    """
    Gets a movie as input and deletes it from the movies dictionary, if it's exist
    :return: None
    """
    movies = storage.list_movies()

    movie_to_delete = green_input("Enter movie name to delete: ")

    if movies.get(movie_to_delete):
        storage.delete_movie(movie_to_delete)
        print(f"Movie {movie_to_delete} successfully deleted.")
    else:
        print(red_text(f"That movie doesn't exist."))



def update_movie():
    """
    Gets a movie name and if it's in the movie dictionary, gets a new rating and updates it
    :return: None
    """
    movies = storage.list_movies()

    movie_to_update = green_input("Enter movie name: ")

    if movie_to_update in movies:
        while True:
            new_movie_rating = green_input("Enter new movie rating: ")

            if is_valid_rating(new_movie_rating):
                break
            else:
                print(red_text("Invalid input, try again."))

        storage.update_movie(movie_to_update, float(new_movie_rating))
        print(f"Movie {movie_to_update} successfully updated.")
    else:
        print(red_text(f"Movie {movie_to_update} doesn't exist."))


def print_stats():
    """
    prints out the average and median ratings and the best and worst movie
    :return: None
    """
    movies = storage.list_movies()

    ratings = []
    for movie in movies:
        ratings.append(movies[movie]["rating"])

    average = sum(ratings) / len(movies)

    print(f"Average rating: \t{round(average, 2)}")

    ratings.sort()

    median = 0
    middle = len(movies) / 2
    # check if the list length is even
    if len(movies) % 2 == 0:
        # add the two middle numbers and divide them by 2
        median = (ratings[int(middle)] + ratings[int(middle) - 1]) / 2
    else:
        median = ratings[int(middle)]

    print(f"Median rating: \t\t{round(median, 2)}")
    print()

    sorted_names = sorted(movies.keys(), key=lambda key: movies[key]["rating"])
    best_count = ratings.count(max(ratings))
    worst_count = ratings.count(min(ratings))

    if best_count > 1:
        best_movies = sorted_names[-best_count:]

        print("Best movies:")
        for movie in best_movies:
            print(get_movie_text(movie))
    else:
        best_movie = max(movies, key=lambda key: movies[key]["rating"])
        print(f"Best movie: \t{get_movie_text(best_movie)}")

    print()

    if worst_count > 1:
        worst_movies = sorted_names[:worst_count]
        print("Worst movies:")
        for movie in worst_movies:
            print(get_movie_text(movie))
    else:
        worst_movie = min(movies, key=lambda key: movies[key]["rating"])
        print(f"Worst movie: \t{get_movie_text(worst_movie)}")


def random_movie():
    """
    Gets a random movie and prints it
    :return: None
    """
    movies = storage.list_movies()

    movie_names = list(movies.keys())
    random_index = random.randrange(0, len(movie_names) - 1)
    random_movie_name = movie_names[random_index]

    print(
        f"Your movie for tonight: {random_movie_name} ({movies[random_movie_name]["year"]}), it's rated {movies[random_movie_name]["rating"]}")


def search_movie():
    """
    Gets a user input and searches in the movies dictionary
    :return: None
    """
    movies = storage.list_movies()

    search_input = green_input("Enter part of movie name: ")
    # create a result list to get the length before printing the result
    search_results = []

    print()
    for movie in movies:
        if search_input.lower() in movie.lower():
            search_results.append(movie)

    fuzzy_search = False

    if len(search_results) == 0:
        # fuzzy matching
        for movie in movies:
            if get_edit_distance(search_input, movie) < 3:
                search_results.append(movie)
                fuzzy_search = True
            else:
                # check single words
                movie_words = movie.split()

                for i, word in enumerate(movie_words):
                    if get_edit_distance(search_input, word) < 3:
                        search_results.append(movie)
                        fuzzy_search = True
                        break;
    if fuzzy_search:
        print(f"The movie '{search_input}' doesn't exist. Did you mean:")
    else:
        print(f"{len(search_results)} movies found.")

    print()
    for movie in search_results:
        print(get_movie_text(movie))


def print_sorted_list_rating():
    """
    prints out the movie list, sorted by rating in descending order
    :return: None
    """
    movies = storage.list_movies()

    sorted_names = sorted(movies.keys(), key=lambda key: movies[key]["rating"])

    print()
    for movie in sorted_names[::-1]:
        print(get_movie_text(movie))


def print_sorted_list_release(min_rating = 0, min_year = 0, max_year = 3000):
    """
    prints out the movie list sorted by release
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

    if order_input in ["N", "n"]:
        sorted_names.reverse()

    print()
    for movie in sorted_names[::]:
        if min_year <= movies[movie]["year"] <= max_year and movies[movie]["rating"] >= min_rating:
            print(get_movie_text(movie))


def get_movie_text(title):
    year, rating, poster = storage.get_movie(title)
    return f"{title} ({year}), {rating}"


def filter_movies():
    """
    Gets the minimum and maximum values for the movie list
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
    with open("html_data/index_template.html", "r") as template_file:
        template_content = template_file.read()

    movies = storage.list_movies()

    movies_html_grid = ""

    for movie in movies:
        movies_html_grid += get_html_movie(movie)

    website_title = "Movie Database"

    website_content = template_content.replace("__TEMPLATE_TITLE__", website_title)
    website_content = website_content.replace("__TEMPLATE_MOVIE_GRID__", movies_html_grid)

    with open("html_data/index.html", "w") as index_file:
        index_file.write(website_content)
    print("The website has been successfully generated!")


def get_html_movie(movie_title: str):
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
    Creates a histogram and saves it as a file
    :return: None
    """
    movies = storage.list_movies()

    ratings = []
    for movie in movies:
        ratings.append(movies[movie]["rating"])

    plt.hist(ratings)

    name_input = green_input("Enter the name of the file: ")

    plt.savefig(f"{name_input}.png")
    print(f"The file was saved under '{name_input}.png'.")


def is_valid_rating(number_string):
    return number_string.replace(".", "", 1).isdigit() and 0 <= float(number_string) <= 10


def get_edit_distance(word, compare_to):
    """
    Gets the difference (distance) between two strings
    :param word: the word to compare
    :param compare_to: the reference word that the other word should compare to
    :return: The difference (distance) as an int
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
            # the word is too short
            word_list.append(compare_to[i])
        elif i < len(word_list) - 1 and word_list[i + 1] == char:
            # there is a letter too much
            del word_list[i]

        elif i < len(compare_to) - 1 and word_list[i] == compare_to[i + 1]:
            # there is a missing letter
            word_list.insert(i, compare_to[i])
        else:
            # there is a wrong letter
            word_list[i] = char

    if len(word_list) > len(compare_to):
        # the word is too long
        distance += len(word_list) - len(compare_to)

    return distance


def quit_program():
    print("Bye!")
    quit()


MENU_OPTIONS = {
    0 : (quit_program, "Exit"),
    1 : (print_movie_list, "List movies"),
    2 : (add_movie, "Add movie"),
    3 : (delete_movie, "Delete movie"),
    4 : (update_movie, "Update movie"),
    5 : (print_stats, "Stats"),
    6 : (random_movie, "Random movie"),
    7 : (search_movie, "Search movie"),
    8 : (print_sorted_list_rating, "Movies sorted by rating"),
    9 : (print_sorted_list_release, "Movies sorted by release"),
    10 : (filter_movies, "Filter movies"),
    11 : (generate_website, "Generate website"),
    12 : (create_histogram, "Create rating histogram")
}


def main():
    """
    The main function
    :return: None
    """

    print_title("Movie Database")

    while True:
        menu()


if __name__ == "__main__":
    main()