from services.spotify_funtions import get_token, get_artists, get_albums, get_songs_from_album, get_available_markets #, get_songs

def get_market_data():
    token = get_token()
    markets = get_available_markets(token)
    return markets

def get_artist_data(artist_name, market=None):
    token = get_token()
    artists = get_artists(token, artist_name, market)
    return artists

def get_album_data(artist_id):
    token = get_token()
    albums = get_albums(token, artist_id)
    return albums
        
# def get_song_data(artist_id):
#     token = get_token()
#     songs = get_songs(token, artist_id)
#     song_info = []
                    
#     for song in songs:
#         song_data = {
#             'song_id': song['song_id'],
#             'song_name': song['song_name'],
#             'interpreters_name': song['interpreters_name'],
#             'composers_name': song['composers_name'],
#             'producers_name': song['producers_name'],
#             'duration': song['duration'],
#             'release_date': song['release_date'],
#             'isrc': song['isrc'],
#             'popularity': song['popularity'],
#             'spotify_url': song['spotify_url'],
#             'itunes_link': song['itunes_link'],
#             'tidal_link': song['tidal_link'],
#             'amazon_link': song['amazon_link'],
#             'deezer_link': song['deezer_link'],
#             'youtube_link': song['youtube_link'],
#             'album_id': song['album_id']
#         }
#         song_info.append(song_data)

#     return song_info

def get_song_data_album(album_id):
    token = get_token()
    songs = get_songs_from_album(token, album_id)
    return songs