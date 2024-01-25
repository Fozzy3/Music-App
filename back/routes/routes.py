from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from cryptography.fernet import Fernet
from schemas.spotify_data import ArtistInfo, AlbumInfo, SongInfo
from services.get import get_artist_data, get_album_data, get_song_data_album, get_market_data
from services.save import save_artist_data_to_db, save_album_data_to_db, save_song_data_to_db
from services.save import check_artist_exists_in_db, get_album_info_from_db, get_song_info_from_db

key = Fernet.generate_key()
f = Fernet(key)

music = APIRouter()

@music.get("/spotify_markets", tags=["SpotifyMarkets"])
def get_market_data_route():
    try:
        market_data = get_market_data()
        return market_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/spotify_artists/{artist_name}", response_model=List[ArtistInfo], tags=["SpotifyArtists"])
def get_artist_data_route(artist_name: str, market: Optional[str] = Query(None)):
    try:
        artist_data = get_artist_data(artist_name, market)
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


@music.get("/spotify_songs_album", response_model=List[SongInfo], tags=["SpotifySongs"])
def get_song_album_data_route(album_ids: List[str] = Query(...)):
    try:
        song_data = []
        for album_id in album_ids:
            song_data.extend(get_song_data_album(album_id))
        return song_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/artist_exists/{artist_id}", response_model=bool, tags=["ArtistExists"])
def artist_exists_route(artist_id: str):
    try:
        artist_exists = check_artist_exists_in_db(artist_id)
        return artist_exists
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/artist_albums_songs/{artist_id}", response_model=Dict[str, Any], tags=["ArtistAlbumsSongs"])
def get_artist_albums_songs_route(artist_id: str):
    try:
        album_info = get_album_info_from_db(artist_id)
        song_info = get_song_info_from_db(artist_id)
        return {"album_info": album_info, "song_info": song_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@music.get("/spotify_songs/{album_id}", response_model=List[SongInfo], tags=["SpotifySongs"])
def get_song_data_route(album_id: str):
    try:
        song_data = get_song_data_album(album_id)
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


