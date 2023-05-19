import sqlite3
from create_database import track_table
from pull_data import get_playlists
from datetime import datetime


def populate_playlist_songs(playlist_id,api_respnse:dict[str,list[dict[str,dict[str,str]]]]) -> None:
    """
    Takes the data from the API and feeds it into the database.
    """
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()

    items = api_respnse
    i = 0
    print(api_respnse)
    print(items)
    # for item in items:
    #     track_id = item
    #     print(track_id)
    #     if i > 5:
    #         break
    #     i += 1
        # cur.execute("INSERT INTO playlist_songs (playlist_id, track_id) VALUES (?,?)", (playlist_id,track_id))

    con.commit()
    con.close()


def populate_songs(song_ids:list) -> None:
    pass


def populate_owner_db(owner_data:list[tuple[str,str,datetime]]):
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()

    for line in owner_data:
        cur.execute("INSERT OR IGNORE INTO owners (playlist_id, owner_name, date) VALUES (?,?,?)", line)

    con.commit()
    con.close()


if __name__ == "__main__":
    owner_data  = get_playlists()
    populate_owner_db(owner_data)
