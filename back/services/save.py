from sqlalchemy.orm import sessionmaker
from models.user import table_artists, table_albums, table_songs
from config.db import meta, engine
from services.spotify_funtions import get_albums, get_artist, get_songs
from schemas.spotify_data import ArtistInfo, AlbumInfo, SongInfo
from typing import Dict



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#def save_artist_data_to_db(artist_name, data):
#    db = SessionLocal()
#    db_spotify_data = SpotifyData(artist_name=artist_name, data=data)
#    db.add(db_spotify_data)
#    db.commit()
#    db.refresh(db_spotify_data)

#def get_spotify_data(artist_name):
#    try:
#        token = get_token()
#        result = artist(token, artist_name)
#        if not result:
#            return {"error": f"No se encontró el artista con el nombre {artist_name}"}

#        artist_id = result["id"]
#        albums = get_albums(token, artist_id)
#        albums_info = []

#        for idx, album in enumerate(albums):
#            album_data = {
#                'index': idx + 1,
#                'name': album['name'],
#                'release_date': album['release_date'],
#                'album_type': album['album_type'],
#                'available_markets': album['available_markets'],
#                'copyright_holders': album['copyright_holders'],
#                'upc': album['upc']
#            }
#            albums_info.append(album_data)

        # Guarda los resultados en la base de datos
#       save_spotify_data_to_db(artist_name, {"artist_info": result, "albums": albums_info})

#        return {"artist_info": result, "albums": albums_info}
#    except Exception as e:
#        return {"error": str(e)}
    
    
