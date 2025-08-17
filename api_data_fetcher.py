import os
from dotenv import load_dotenv

def get_movie_data_from_api(title: str):
    load_dotenv()
    api_key = os.getenv("API_KEY")

    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

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