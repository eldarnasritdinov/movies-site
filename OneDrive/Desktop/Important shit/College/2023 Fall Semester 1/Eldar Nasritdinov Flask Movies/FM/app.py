from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Define the database file
DATABASE = 'db_data_transform.db'  # Replace with your database name

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route for the home page
@app.route('/', methods=['GET'])
def display_movies():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT movies.title, genres.name AS genre_name, movies.year
        FROM movies
        JOIN connections ON movies.id = connections.movie_id
        JOIN genres ON connections.genre_id = genres.id
    """
    cursor.execute(query)
    movies = cursor.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/', methods=['POST'])
def filter_movies():
    conn = get_db_connection()
    cursor = conn.cursor()

    selected_genre = request.form['genre']
    if selected_genre:
        query = """
            SELECT movies.title, genres.name AS genre_name, movies.year
            FROM movies
            JOIN connections ON movies.id = connections.movie_id
            JOIN genres ON connections.genre_id = genres.id
            WHERE genres.id = ?
        """
        cursor.execute(query, (selected_genre,))
    else:
        query = """
            SELECT movies.title, genres.name AS genre_name, movies.year
            FROM movies
            JOIN connections ON movies.id = connections.movie_id
            JOIN genres ON connections.genre_id = genres.id
        """
        cursor.execute(query)

    movies = cursor.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)

