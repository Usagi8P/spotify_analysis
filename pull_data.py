import spotipy #type: ignore
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth #type: ignore
from api_setup import logger_setup, set_env_variables
from datetime import datetime
from typing import Any


def get_playlists() -> list[tuple[str,str,datetime]]:
    """
    Reads playlist codes from the secrets folder and loads them into a list.
    """
    owner_data: list[tuple[str,str,datetime]] = []

    with open('secrets/playlists.txt','r') as f:
        lines = f.readlines() 

        for line in lines:
            playlist_id = line[line.find('=')+1:-1]
            name = line[0:line.find('_')]
            stored_date = line[line.find('_')+1:line.find('=')]
            playlist_date = datetime.strptime(stored_date, '%b_%y')
            if playlist_id:
                owner_data.append((playlist_id,name.capitalize(),playlist_date))
    
    return owner_data


def get_songs_in_playlist(sp:spotipy.Spotify, pl_id:str):
    """
    Pulls the songs for a single playlist.
    """
    offset = 0

    response = sp.playlist_items(pl_id,
                                offset=offset,
                                fields='items.track.id,total',
                                additional_types=['track'])

    return response


def create_total_track_list(sp:spotipy.Spotify) -> set[str]:
    platlist_data = get_playlists()

    track_ids: set[str] = set()
    for playlist in platlist_data:
        response = get_songs_in_playlist(sp,playlist[0])

        for item in response['items']:
            track_ids.add(item['track']['id'])

    return track_ids


def create_new_playlist(sp_personal) -> str:
    with open('secrets/username.txt','r') as f:
        username = f.readline()

    new_playlist = sp_personal.user_playlist_create(username,'Full Playlist')
    
    with open('secrets/playlist_id.txt','w') as f:
        f.write(new_playlist['id'])

    return new_playlist['id']


def get_new_playlist_id(sp_personal) -> str:
    try:
        with open('secrets/playlist_id.txt','r') as f:
            playlist_id = f.readline()
    except:
        return create_new_playlist(sp_personal)

    if playlist_id:
        return playlist_id
    return create_new_playlist(sp_personal)

def get_song_properties(sp: spotipy.Spotify, track_ids: set[str]) -> list[dict[str,Any]]:
    track_list: list[str] = list(track_ids)
    n_tracks = len(track_list)
    track_features: list[dict[str,Any]] = []

    analysed_tracks: int = 0
    while analysed_tracks < n_tracks-1:
        response = sp.audio_features(track_list[analysed_tracks:analysed_tracks+99])
        analysed_tracks += 99
        track_features += response

    return track_features
