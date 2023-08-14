import sqlite3


fake_names_table = '''CREATE TABLE IF NOT EXISTS fake_names
                      (owner_name TEXT PRIMARY KEY,
                       fake_name TEXT)'''

owner_table = '''CREATE TABLE IF NOT EXISTS owners
                 (playlist_id TEXT PRIMARY KEY,
                  owner_name TEXT,
                  date DATE)'''

track_table = '''CREATE TABLE IF NOT EXISTS songs
                 (track_id TEXT PRIMARY KEY,
                  analysis_url TEXT,
                  acousticness REAL CHECK (acousticness >= 0 AND acousticness <= 1),
                  danceability REAL CHECK (danceability >= 0 AND danceability <= 1),
                  duration_ms REAL,
                  energy REAL CHECK (energy >= 0 AND energy <= 1),
                  instrumentalness REAL CHECK (instrumentalness >= 0 AND instrumentalness <= 1),
                  key INTEGER,
                  liveness REAL CHECK (liveness >= 0 AND liveness <= 1),
                  loudness REAL,
                  speachiness REAL CHECK (speachiness >= 0 AND speachiness <= 1),
                  tempo REAL,
                  time_signature INTEGER,
                  valence REAL CHECK (valence >= 0 AND valence <= 1))'''

playlist_songs = '''CREATE TABLE IF NOT EXISTS playlist_songs
                    (playlist_id INTEGER,
                     track_id INTEGER,
                     PRIMARY KEY (playlist_id, track_id),
                     FOREIGN KEY (playlist_id) REFERENCES owners(playlist_id),
                     FOREIGN KEY (track_id) REFERENCES songs(track_id))'''


def create_database() -> None:
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    cur.execute(fake_names_table)
    cur.execute(owner_table)
    cur.execute(track_table)
    cur.execute(playlist_songs)
    con.commit()
    con.close()


if __name__ == "__main__":
    create_database()
