from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from models.user import table_artists, table_albums, table_songs
from config.db import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_artist_data_to_db(artist_data):
    db = SessionLocal()
    stmt = insert(table_artists).values(
        artist_id=artist_data['artist_id'], 
        artist_name=artist_data['artist_name'],
        popularity=artist_data['popularity'],
        followers=artist_data['followers']
    )
    db.execute(stmt)
    db.commit()

def save_album_data_to_db(album_data):
    db = SessionLocal()
    stmt = insert(table_albums).values(
        album_id=album_data['album_id'], 
        album_name=album_data['album_name'],
        album_type=album_data['album_type'],
        release_date=album_data['release_date'],
        available_markets=album_data['available_markets'],
        num_available_markets=album_data['num_available_markets'],
        popularity=album_data['popularity'],
        cover_image=album_data['cover_image'],
        upc=album_data['upc'],
        copyright_c=album_data['copyright_c'],
        copyright_p=album_data['copyright_p'],
        artist_id=album_data['artist_id']
    )
    db.execute(stmt)
    db.commit()

def save_song_data_to_db(song_data):
    db = SessionLocal()
    stmt = insert(table_songs).values(
        song_id=song_data['song_id'],
        song_name=song_data['song_name'],
        interpreters_name=song_data['interpreters_name'],
        composers_name=song_data['composers_name'],
        producers_name=song_data['producers_name'],
        duration=song_data['duration'],
        release_date=song_data['release_date'],
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
    db.execute(stmt)
    db.commit()
    
#Verificación de existencia de datos en la base de datos

def check_artist_exists_in_db(artist_id):
    db = SessionLocal()
    stmt = table_artists.select().where(table_artists.c.artist_id == artist_id)
    result = db.execute(stmt)
    return result.rowcount > 0  # True si existe, False si no existe    

#Obtención de datos de la base de datos

def get_album_info_from_db(artist_id):
    db = SessionLocal()
    stmt = table_albums.select().where(table_albums.c.artist_id == artist_id)
    result = db.execute(stmt)
    return result.fetchall()

def get_song_info_from_db(artist_id):
    db = SessionLocal()
    # Obtén los álbumes del artista
    albums = get_album_info_from_db(artist_id)

    # Para cada álbum, obtén las canciones
    songs = []
    for album in albums:
        stmt = table_songs.select().where(table_songs.c.album_id == album['album_id'])
        result = db.execute(stmt)
        album_songs = result.fetchall()
        songs.extend(album_songs)

    return songs
