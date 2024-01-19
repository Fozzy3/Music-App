from sqlalchemy import Integer, String, Table, Column, Date, ForeignKey, JSON
from config.db import meta, engine


table_artists = Table('artists', meta, 
        Column('artist_id', String(255), primary_key=True), 
        Column('artist_name', String(100)),
        Column('popularity', Integer),
        Column('followers', Integer)
)

table_albums = Table('albums', meta, 
        Column('album_id', String(255), primary_key=True), 
        Column('album_name', String(100)),
        Column('album_type', String(100)),
        Column('release_date', Date),
        Column('available_markets', JSON),
        Column('num_available_markets', Integer),
        Column('genres', JSON),  
        Column('popularity', Integer),
        Column('cover_image', String(255)),
        Column('upc', String(255)),
        Column('copyright_c', JSON),
        Column('copyright_p', JSON),
        Column('artist_id', String(255), ForeignKey('artists.artist_id'))
)

table_songs = Table('songs', meta, 
        Column('song_id', String(255), primary_key=True), 
        Column('song_name', String(100)),
        Column('interpreters_name', String(255)),
        Column('composers_name', String(255)),
        Column('producers_name', String(255)),
        Column('duration', Integer),
        Column('release_year', Integer),
        Column('isrc', String(255)),
        Column('popularity', Integer),
        Column('spotify_url', String(255)),
        Column('itunes_link', String(255)),
        Column('tidal_link', String(255)),
        Column('amazon_link', String(255)),
        Column('deezer_link', String(255)),
        Column('youtube_link', String(255)),
        Column('album_id', String(255), ForeignKey('albums.album_id'))
)

meta.create_all(engine)
