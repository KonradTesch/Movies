import os
import requests
from dotenv import load_dotenv

api_key = ""

def set_api_key():
    """
    Load the api key from the env file and sets the global variable.
    :return:
    """
    load_dotenv()
    global api_key
    api_key = os.getenv("API_KEY")

class APIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"APIError: {message}")

    def __str__(self):
        return f"APIError: {self.message}"


def get_movie_data_from_api(title: str):
    """
    Fetches title, release year, rating and pooster url from the OMDb API.
    :params title: The movie title.
    :return: Dictionary with the movie data.
    """
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

    response = requests.get(url)

    response_data = response.json()

    if response_data.get("Error"):
        error_message = response_data["Error"]
        raise APIError(error_message)

    movie_data = {"title": response_data["Title"],
                  "year": response_data["Year"],
                  "rating": response_data["imdbRating"],
                  "posterURL": response_data["Poster"]}

    return movie_data