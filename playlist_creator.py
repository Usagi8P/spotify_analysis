import spotipy #type: ignore
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth #type: ignore
from api_setup import logger_setup, set_env_variables
import sqlite3

from pull_data import get_playlists, get_songs_in_playlist, get_song_properties, get_new_playlist_id
from create_database import create_database
from populate_database import populate_owner_db, populate_playlist_songs, populate_track_features


def setup_spotify() -> tuple[spotipy.Spotify,spotipy.Spotify]:
    logger_setup()
    set_env_variables()

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope='playlist-modify-public'
    sp_personal = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return sp_personal, sp

def update_song_data() -> None:
    """
    Updates the local database with spotify data.
    """
    create_database()
    sp_personal, sp = setup_spotify()

    owner_data = get_playlists()
    populate_owner_db(owner_data)

    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    owner_playlist_req = cur.execute("""SELECT playlist_id FROM owners""")
    owner_playlist_ids = owner_playlist_req.fetchall()
    con.close()

    for playlist_id in owner_playlist_ids:
        response = get_songs_in_playlist(sp,playlist_id[0])
        populate_playlist_songs(playlist_id[0], response)

    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    playlist_songs_req = cur.execute("""SELECT track_id FROM playlist_songs""")
    playlist_track_ids:list[tuple[str,None]] = playlist_songs_req.fetchall()
    song_req = cur.execute("""SELECT track_id FROM songs""")
    song_track_ids:list[tuple[str,None]] = song_req.fetchall()
    con.close()

    new_songs: set[str] = set()
    for playlist_track in playlist_track_ids:
        if playlist_track[0] not in [song_track[0] for song_track in song_track_ids]:
            new_songs.add(playlist_track[0])

    track_features = get_song_properties(sp, new_songs)

    populate_track_features(track_features)


def playlist_creator() -> None:
    """
    Creates new playlist and populates it with songs in the database.
    """
    sp_personal, sp = setup_spotify()

    new_playlist_id = get_new_playlist_id(sp_personal)

    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    all_tracks = cur.execute("""SELECT track_id FROM songs""").fetchall()
    con.close()

    final_tracklist = [song_track[0] for song_track in all_tracks]
    n_tracks = len(final_tracklist)
    
    if n_tracks <= 100:
        sp_personal.playlist_replace_items(new_playlist_id,final_tracklist)
    else:
        uploaded_tracks: int = 0
        sp_personal.playlist_replace_items(new_playlist_id,final_tracklist[uploaded_tracks:uploaded_tracks+99])
        uploaded_tracks += 99

        while uploaded_tracks + 99 <= n_tracks - 1:
            sp_personal.playlist_add_items(new_playlist_id,final_tracklist[uploaded_tracks:uploaded_tracks+99])
            uploaded_tracks += 99
        
        if uploaded_tracks < n_tracks - 1:
            sp_personal.playlist_add_items(new_playlist_id,final_tracklist[uploaded_tracks:n_tracks-1])


if __name__=="__main__":
    update_song_data()
    playlist_creator()