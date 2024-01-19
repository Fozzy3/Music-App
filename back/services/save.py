from sqlalchemy.orm import sessionmaker
from models.user import table_artists, table_albums, table_songs
from config.db import engine
from services.spotify_funtions import get_albums, get_artist, get_songs, get_token


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_artist_data(artist_name):
        try:
                # Obtén el token
                token = get_token()
                                                
                # Llama a la función get_artist
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
        except Exception as e:
                return {
                "artista": [{
                        'artist_id': None,
                        'artist_name': None,
                        'popularity': None,
                        'followers': None,
                        'error': str(e)
                }]
                }
                        
def get_album_data(artist_id):
        try:
                # Obtén el token
                token = get_token()
                                
                # Llama a la función get_albums
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
        except Exception as e:
                return {
                        "album": [{
                        'album_id': None,
                        'album_name': None,
                        'album_type': None,
                        'release_date': None,
                        'available_markets': None,
                        'num_available_markets': None,
                        'popularity': None,
                        'cover_image': None,
                        'upc': None,
                        'copyright_c': None,
                        'copyright_p': None,
                        'artist_id': None,
                        'error': str(e)
                }]
                }

def get_song_data(artist_id):
        try:
                # Obtén el token
                token = get_token()
                                
                # Llama a la función get_songs
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
        except Exception as e:
                return {
                        "song": [{
                        'song_id': None,
                        'song_name': None,
                        'interpreters_name': None,
                        'composers_name': None,
                        'producers_name': None,
                        'duration': None,
                        'release_date': None,
                        'isrc': None,
                        'popularity': None,
                        'spotify_url': None,
                        'itunes_link': None,
                        'tidal_link': None,
                        'amazon_link': None,
                        'deezer_link': None,
                        'youtube_link': None,
                        'album_id': None,
                        'error': str(e)
                }]
                }

#Guardado de datos en la base de datos

def save_artist_data_to_db(artist_data):
        db = SessionLocal()
        db_artist_data = table_artists(
                artist_id=artist_data['artist_id'], 
                artist_name=artist_data['artist_name'],
                popularity=artist_data['popularity'],
                followers=artist_data['followers']
        )
        db.add(db_artist_data)
        db.commit()
        db.refresh(db_artist_data)

def save_album_data_to_db(album_data):
        db = SessionLocal()
        db_album_data = table_albums(
                album_id=album_data['album_id'], 
                album_name=album_data['album_name'],
                album_type=album_data['album_type'],
                release_date=album_data['release_date'],
                available_markets=album_data['available_markets'],
                num_available_markets=album_data['num_available_markets'],
                genres=album_data['genres'],
                popularity=album_data['popularity'],
                cover_image=album_data['cover_image'],
                upc=album_data['upc'],
                copyright_c=album_data['copyright_c'],
                copyright_p=album_data['copyright_p'],
                artist_id=album_data['artist_id']
        )
        db.add(db_album_data)
        db.commit()
        db.refresh(db_album_data)

def save_song_data_to_db(song_data):
        db = SessionLocal()
        db_song_data = table_songs(
                song_id=song_data['song_id'], 
                song_name=song_data['song_name'],
                interpreters_name=song_data['interpreters_name'],
                composers_name=song_data['composers_name'],
                producers_name=song_data['producers_name'],
                duration=song_data['duration'],
                release_year=song_data['release_year'],
                isrc=song_data['isrc'],
                popularity=song_data['popularity'],
                spotify_url=song_data['spotify_url'],
                itunes_link=song_data['itunes_link'],
                tidal_link=song_data['tidal_link'],
                amazon_link=song_data['amazon_link'],
                deezer_link=song_data['deezer_link'],
                youtube_link=song_data['youtube_link'],
                album_id=song_data['album_id']
        )
        db.add(db_song_data)
        db.commit()
        db.refresh(db_song_data)