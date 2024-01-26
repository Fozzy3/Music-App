from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from cryptography.fernet import Fernet
from schemas.spotify_data import ArtistInfo, AlbumInfo, SongInfo
from services.get import get_artist_data, get_album_data, get_song_data_album
from services.save import save_artist_data_to_db, save_album_data_to_db, save_song_data_to_db, album_exists_in_db, artist_exists_in_db

key = Fernet.generate_key()
f = Fernet(key)

music = APIRouter()


@music.get("/spotify_artists/{artist_name}", response_model=List[ArtistInfo], tags=["Artists"])
def get_artist_data_route(artist_name: str, market: Optional[str] = Query(None)):
    try:
        artist_data = get_artist_data(artist_name, market)
        return artist_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/artist_exists/{artist_id}", response_model=bool, tags=["Artists"])
def artist_exists_route(artist_id: str):
    try:
        artist_data = {'artist_id': artist_id}  
        artist_exists = artist_exists_in_db(artist_data)  
        return artist_exists
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.post("/save_artist_data", tags=["Artists"])
def save_artist_data_route(artist_data: dict):
    try:
        if artist_exists_in_db(artist_data):
            return {"message": "Artist already exists in the database"}
        save_artist_data_to_db(artist_data)
        return {"message": "Artist data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@music.get("/spotify_albums/{artist_id}", response_model=List[AlbumInfo], tags=["Albums"])
def get_album_data_route(artist_id: str):
    try:
        album_data = get_album_data(artist_id)
        return album_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.post("/save_album_data", tags=["Albums"])
def save_album_data_route(album_data: List[dict]):
    try:
        for album in album_data:
            artist_data = {'artist_id': album['artist_id']}  # Crear un diccionario con el artist_id
            if not artist_exists_in_db(artist_data):  # Llamar a la función con el diccionario
                return {"message": "Artist not found in the database. Please save the artist first."}
            if album_exists_in_db(album):
                continue
            save_album_data_to_db(album)
            songs = get_song_data_album(album['album_id'])
            for song in songs:
                save_song_data_to_db(song)
        return {"message": "Album and song data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    


@music.get("/spotify_songs/{album_id}", response_model=List[SongInfo], tags=["Songs"])
def get_song_data_route(album_id: str):
    try:
        song_data = get_song_data_album(album_id)
        return song_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
