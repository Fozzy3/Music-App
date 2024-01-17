from typing import Optional, Any, List
from pydantic import BaseModel

class ArtistInfo(BaseModel):
    external_urls: dict
    followers: dict
    genres: List[str]
    href: str
    id: str
    images: List[dict]
    name: str
    popularity: int
    type: str
    uri: str

class AlbumInfo(BaseModel):
    index: int
    name: str
    release_date: str
    album_type: str
    available_markets: int
    copyright_holders: List[Any]
    upc: str

class SpotifyDataResponse(BaseModel):
    artist_info: Optional[ArtistInfo]
    albums: Optional[List[AlbumInfo]]
