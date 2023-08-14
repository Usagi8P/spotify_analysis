import sqlite3
from create_database import track_table
from pull_data import get_playlists
from datetime import datetime
from typing import Any


def populate_playlist_songs(playlist_id,api_response:dict[str,list[dict[str,dict[str,str]]]]) -> None:
    """
    Takes the data from the API and feeds it into the database.
    """
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()

    for item in api_response['items']:
        cur.execute("""INSERT OR IGNORE INTO playlist_songs
            (playlist_id, track_id) VALUES (?,?)""",
            (playlist_id,item['track']['id']))
        
    con.commit()
    con.close()


def populate_track_features(track_features:list[dict[str,Any]]) -> None:
    """
    Adds track feature information to the database.
    """
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()

    for item in track_features:
        cur.execute("""INSERT OR IGNORE INTO songs
            (track_id, analysis_url, acousticness, danceability, duration_ms,
             energy, instrumentalness, key, liveness, loudness,
             speechiness, tempo, time_signature, valence) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (item['id'],item['analysis_url'],item['acousticness'],item['danceability'],item['duration_ms'],
             item['energy'],item['instrumentalness'],item['key'],item['liveness'],item['loudness'],
             item['speechiness'],item['tempo'],item['time_signature'],item['valence']))
        
    con.commit()
    con.close()



def populate_owner_db(owner_data:list[tuple[str,str,datetime]]):
    """
    Populates information into the list of playlists and their respective owners.
    """
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()

    for line in owner_data:
        cur.execute("""INSERT OR IGNORE INTO owners
                       (playlist_id, owner_name, date) VALUES (?,?,?)""",
                       line)

    con.commit()
    con.close()
