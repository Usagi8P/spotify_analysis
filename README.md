# Spotify Analysis
This project is used to collect playlists into a single total playlist.
Then it gets the track features to be used in analysis seen in `spotify_analyis.ipynb`.
The inspiration and overview for this project can be found in this [Medium article](https://medium.com/@Usagi8P/using-the-spotify-api-to-combine-playlists-16b59717a686).

In order for the program to know which playlists to combine the Playlist IDs of the to be combined playlists needs to be supplied in a `playlists.txt` file in the `secrets` folder.
There program assumes that each playlist is associated with a month and a year.
In order for parsing of the file to complete successfully please follow the file structure supplied in `secrets_sample`.