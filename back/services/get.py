from services.spotify_funtions import get_token, get_artist, get_albums, get_songs_from_album, get_songs

def get_artist_data(artist_name):
    token = get_token()
    artists = get_artist(token, artist_name)
    artist_info = []

    for artist in artists:
        artist_data = {
            'artist_id': artist['artist_id'],
            'artist_name': artist['artist_name'],
            'popularity': artist['popularity'],
            'followers': artist['followers']
        }
        artist_info.append(artist_data)

    return artist_info

def get_album_data(artist_id):
    token = get_token()
    albums = get_albums(token, artist_id)
    album_info = []

    for album in albums:
        album_data = {
            'album_id': album['album_id'],
            'album_name': album['album_name'],
            'album_type': album['album_type'],
            'release_date': album['release_date'],
            'available_markets': album['available_markets'],
            'num_available_markets': album['num_available_markets'],
            'popularity': album['popularity'],
            'cover_image': album['cover_image'],
            'upc': album['upc'],
            'copyright_c': album['copyright_c'],
            'copyright_p': album['copyright_p'],
            'artist_id': album['artist_id']
        }
        album_info.append(album_data)

    return album_info
        
def get_song_data(artist_id):
    token = get_token()
    songs = get_songs(token, artist_id)
    song_info = []
                    
    for song in songs:
        song_data = {
            'song_id': song['song_id'],
            'song_name': song['song_name'],
            'interpreters_name': song['interpreters_name'],
            'composers_name': song['composers_name'],
            'producers_name': song['producers_name'],
            'duration': song['duration'],
            'release_date': song['release_date'],
            'isrc': song['isrc'],
            'popularity': song['popularity'],
            'spotify_url': song['spotify_url'],
            'itunes_link': song['itunes_link'],
            'tidal_link': song['tidal_link'],
            'amazon_link': song['amazon_link'],
            'deezer_link': song['deezer_link'],
            'youtube_link': song['youtube_link'],
            'album_id': song['album_id']
        }
        song_info.append(song_data)

    return song_info

def get_song_data_album(album_id):
    token = get_token()
    songs = get_songs_from_album(token, album_id)
    song_info = []
                    
    for song in songs:
        song_data = {
            'song_id': song['song_id'],
            'song_name': song['song_name'],
            'interpreters_name': song['interpreters_name'],
            'composers_name': song['composers_name'],
            'producers_name': song['producers_name'],
            'duration': song['duration'],
            'release_date': song['release_date'],
            'isrc': song['isrc'],
            'popularity': song['popularity'],
            'spotify_url': song['spotify_url'],
            'itunes_link': song['itunes_link'],
            'tidal_link': song['tidal_link'],
            'amazon_link': song['amazon_link'],
            'deezer_link': song['deezer_link'],
            'youtube_link': song['youtube_link'],
            'album_id': song['album_id']
        }
        song_info.append(song_data)

    return song_info