import spotipy #type: ignore
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth #type: ignore
from api_setup import logger_setup, set_env_variables


def get_playlists() -> list[str]:
    # Reads playlist codes from the secrets folder and loads them into a list
    playlists: list[str] = []

    with open('secrets/playlists.txt','r') as f:
        lines = f.readlines() 

        for line in lines:
            playlist_id = line[line.find('=')+1:-1]
            if playlist_id:
                playlists.append(playlist_id)
    
    return playlists


def get_songs_in_playlist(sp,pl_id):
    offset = 0

    response = sp.playlist_items(pl_id,
                                offset=offset,
                                fields='items.track.id,total',
                                additional_types=['track'])

    return response


def create_total_track_list(sp) -> set[str]:
    playlists: list[str] = get_playlists()

    track_ids: set[str] = set()
    for playlist in playlists:
        response = get_songs_in_playlist(sp,playlist)

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