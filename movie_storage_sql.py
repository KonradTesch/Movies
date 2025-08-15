from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

def create_movies_table():
    # Create the movies table if it does not exist
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL
            )
        """))
        connection.commit()

def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as con:
        result = con.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}

def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.connect() as con:
        try:
            con.execute(text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                               {"title": title, "year": year, "rating": rating})
            con.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as con:
        try:
            query = """
                    DELETE FROM movies
                    WHERE title = :title
                    """
            parameters = {"title": title}

            con.execute(text(query), parameters= parameters)
            con.commit()
            print(f"Movie '{title}' deleted successfully..")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as con:
        try:
            query = """
                    UPDATE movies 
                    SET rating = :rating
                    WHERE title = :title
                    """
            parameters = {"rating" : rating, "title" : title}

            con.execute(text(query), parameters= parameters)
            con.commit()
            print(f"Movie '{title}' updated successfully..")
        except Exception as e:
            print(f"Error: {e}")


def get_movie(title):
    """Get a single movie from the database."""
    with engine.connect() as con:
        try:
            query = """
                    SELECT title, year, rating FROM movies 
                    WHERE title = :title
                    """
            parameters = {"title" : title}

            result = con.execute(text(query), parameters)
            movie = result.fetchall()

            title, year, rating = movie[0][0], movie[0][1], movie[0][2]

            return title, year, rating
        except Exception as e:
            print(f"Error: {e}")