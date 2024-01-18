from typing import List
from pydantic import BaseModel

class ArtistInfo(BaseModel):
    artist_id: str
    artist_name: str
    popularity: int
    followers: int

class AlbumInfo(BaseModel):
    album_id: str
    album_name: str
    album_type: str
    release_date: str
    available_markets: List[str]
    num_available_markets: int
    genres: List[str]
    popularity: int
    cover_image: str
    upc: str
    copyright_c: List[str]
    copyright_p: List[str]
    artist_id: str

class SongInfo(BaseModel):
    song_id: str
    song_name: str
    interpreters_name: str
    composers_name: str
    producers_name: str
    duration: int
    release_year: int
    isrc: str
    popularity: int
    spotify_url: str
    itunes_link: str
    tidal_link: str
    amazon_link: str
    deezer_link: str
    youtube_link: str
    album_id: str

