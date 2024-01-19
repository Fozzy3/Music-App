from fastapi import APIRouter
from cryptography.fernet import Fernet
from schemas.spotify_data import ArtistInfo, AlbumInfo, SongInfo
from services.save import get_artist_data, get_album_data, get_song_data
from typing import List

key = Fernet.generate_key()
f = Fernet(key)

music = APIRouter()

@music.get("/spotify_artists/{artist_name}", response_model=List[ArtistInfo], tags=["SpotifyArtists"])
def get_artist_data_route(artist_name: str):
    try:
        artist_data = get_artist_data(artist_name)
        return artist_data
    except Exception as e:
        return [{"error": str(e)}]

@music.get("/spotify_albums/{artist_id}", response_model=List[AlbumInfo], tags=["SpotifyAlbums"])
def get_album_data_route(artist_id: str):
    try:
        album_data = get_album_data(artist_id)
        return album_data
    except Exception as e:
        return [{"error": str(e)}]

@music.get("/spotify_songs/{artist_id}", response_model=List[SongInfo], tags=["SpotifySongs"])
def get_song_data_route(artist_id: str):
    try:
        song_data = get_song_data(artist_id)
        return song_data
    except Exception as e:
        return [{"error": str(e)}]

