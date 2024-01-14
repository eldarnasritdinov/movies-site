import sqlite3
import pandas as pd

df = pd.read_csv('movies_data.csv')
movie_id = []
title = []
year = []

for i in range(len(df)):

    # ID
    movie_id.append(df['movieId'][i])

    # TITLE
    title.append(" ".join(df['title'][i].split(' ')[:-1]))

    # YEAR
    try:
        year.append(int(df['title'][i].split(' ')[-1:][0][1:-1]))
    except:
        year.append(0)

movies_table = pd.DataFrame({
    'id': movie_id,
    'title': title,
    'year': year
})

genres = []

for i in range(len(df)):
    for j in range (len(df['genres'][i].split("|"))):
        if df['genres'][i].split("|")[j] not in genres:
            genres.append(df['genres'][i].split("|")[j])

genres_table = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'name': genres
})

movie_id = []
genre_id = []

for i in range(len(df)):
    for j in range (len(df['genres'][i].split("|"))):
        movie_id.append(i+1)
        genre = df['genres'][i].split("|")[j]
        genre_id.append(genres_table[ genres_table['name'] == genre ]['id'].iloc[0])

connections_table = pd.DataFrame({
    'movie_id': movie_id,
    'genre_id': genre_id
})

# SQLITE

conn = sqlite3.connect('db_data_transform.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY,
    title VARCHAR,
    year INT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS connections (
    movie_id INT,
    genre_id INT,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS genres (
    id INT PRIMARY KEY,
    name VARCHAR
)
''')

movies_table.to_sql('movies', conn, if_exists='replace', index=False)

connections_table.to_sql('connections', conn, if_exists='replace', index=False)

genres_table.to_sql('genres', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

conn = sqlite3.connect('db_data_transform.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)