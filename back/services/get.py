from services.spotify_funtions import get_token, get_artists, get_albums, get_songs_from_album

def get_artist_data(artist_name, market=None):
    token = get_token()
    artists = get_artists(token, artist_name, market)
    return artists

def get_album_data(artist_id):
    token = get_token()
    albums = get_albums(token, artist_id)
    return albums

def get_song_data_album(album_id):
    token = get_token()
    songs = get_songs_from_album(token, album_id)
    return songs

