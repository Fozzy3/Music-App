from typing import List
from fastapi import APIRouter, HTTPException
from cryptography.fernet import Fernet
from schemas.spotify_data import ArtistInfo, AlbumInfo, SongInfo
from services.get import get_artist_data, get_album_data, get_song_data, get_song_data_album
from services.save import save_artist_data_to_db, save_album_data_to_db, save_song_data_to_db

key = Fernet.generate_key()
f = Fernet(key)

music = APIRouter()

@music.get("/spotify_artists/{artist_name}", response_model=List[ArtistInfo], tags=["SpotifyArtists"])
def get_artist_data_route(artist_name: str):
    try:
        artist_data = get_artist_data(artist_name)
        return artist_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/spotify_albums/{artist_id}", response_model=List[AlbumInfo], tags=["SpotifyAlbums"])
def get_album_data_route(artist_id: str):
    try:
        album_data = get_album_data(artist_id)
        return album_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/spotify_songs_album/{album_id}", response_model=List[SongInfo], tags=["SpotifySongs"])
def get_song_album_data_route(album_id: str):
    try:
        song_data = get_song_data_album(album_id)
        return song_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/spotify_songs/{artist_id}", response_model=List[SongInfo], tags=["SpotifySongs"])
def get_song_data_route(artist_id: str):
    try:
        song_data = get_song_data(artist_id)
        return song_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

#Guardado de datos en la base de datos

@music.post("/save_artist_data", tags=["SaveArtistData"])
def save_artist_data_route(artist_data: dict):
    try:
        save_artist_data_to_db(artist_data)
        return {"message": "Artist data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.post("/save_album_data", tags=["SaveAlbumData"])
def save_album_data_route(album_data: List[dict]):
    try:
        for album in album_data:
            save_album_data_to_db(album)
        return {"message": "Album data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.post("/save_song_data", tags=["SaveSongData"])
def save_song_data_route(song_data: List[dict]):
    try:
        for song in song_data:
            save_song_data_to_db(song)
        return {"message": "Song data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


