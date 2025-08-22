from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)


def list_movies() -> dict:
    """
    Retrieve all movies from the database.
    :return: dictionary with movie titles as keys and year/rating as values
    """
    with engine.connect() as con:
        result = con.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(movie_data: dict):
    """
    Add a new movie to the database.
    :param movie_data: dictionary containing title, year, rating, posterURL
    :return: None
    """
    with engine.connect() as con:
        try:
            con.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"
                ),
                {
                    "title": movie_data["title"],
                    "year": movie_data["year"],
                    "rating": movie_data["rating"],
                    "poster_url": movie_data["posterURL"],
                },
            )
            con.commit()
            print(f"Movie '{movie_data['title']}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title: str):
    """
    Delete a movie from the database.
    :param title: title of the movie to delete
    :return: None
    """
    with engine.connect() as con:
        try:
            query = """
                    DELETE FROM movies
                    WHERE title = :title
                    """
            parameters = {"title": title}

            con.execute(text(query), parameters)
            con.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def get_movie(title: str) -> tuple:
    """
    Get a single movie from the database.
    :param title: title of the movie to retrieve
    :return: tuple containing (year, rating, poster_url) or empty tuple if error
    """
    with engine.connect() as con:
        try:
            query = """
                    SELECT year, rating, poster_url FROM movies 
                    WHERE title = :title
                    """
            parameters = {"title": title}

            result = con.execute(text(query), parameters)
            movie = result.fetchall()

            year, rating, poster = movie[0][0], movie[0][1], movie[0][2]

            return year, rating, poster
        except Exception as e:
            print(f"Error: {e}")
            return ()
