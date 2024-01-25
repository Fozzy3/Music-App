import base64
import json
from dotenv import load_dotenv
import os
from requests import post, get
import requests
from services.song_links import get_song_links
from services.genius_api import get_song_info_by_name_artist


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_auth_header(auth_token):
    """
    Diccionario usado como cabecera para las solicitudes autenticadas a la API.
    """
    if auth_token is None:
        raise ValueError("Token is None")
    return {"Authorization": f"Bearer {auth_token}"}

def get_token():
    """
    Obtención token de acceso de la API de Spotify.
    El token de acceso es necesario para hacer solicitudes autenticadas a la API de Spotify.
    """

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",  
        "Content-Type": "application/x-www-form-urlencoded"  
    }
    data = {"grant_type" : "client_credentials"}

    result = post(url, headers=headers, data=data, timeout=120)
    
    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener el access_token. Código de estado: {result.status_code}. Contenido de la respuesta: {result.content}")

    json_result = json.loads(result.content)
    token = json_result.get("access_token")

    if token is None:
        raise ValueError(f"Error al obtener el access_token. No se encontró el token en la respuesta. Contenido de la respuesta: {result.content}")

    return token

def get_available_markets(token):
    """
    Obtiene todos los mercados disponibles de la API de Spotify.
    """
    base_url = os.getenv('API_SPOTIFY')
    if base_url is None:
        raise ValueError("La variable de entorno API_SPOTIFY no está configurada.")
    
    headers = get_auth_header(token)

    query_url = f"{base_url}/v1/markets"
    result = get(query_url, headers=headers, timeout=300)  

    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los mercados disponibles. Código de estado: {result.status_code}")

    json_result = json.loads(result.content)
    markets = json_result.get("markets")

    if markets is None:
        raise ValueError("No se encontraron mercados en la respuesta.")

    return markets

def get_artists(token, artist_name, market=None):
    """
    Busqueda información sobre los artistas especificados.
    """
    base_url = os.getenv('API_SPOTIFY')
    if base_url is None:
        raise ValueError("La variable de entorno API_SPOTIFY no está configurada.")
    
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=5"
    
    if market is not None:
        query += f"&market={market}"

    query_url = f"{base_url}/search{query}"
    result = get(query_url, headers=headers, timeout=300)  

    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los artistas. Código de estado: {result.status_code}")

    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result)==0:
        raise ValueError("No se encontró ningún artista con ese nombre.")
    
    artists_info = []

    for artist in json_result:
        artist_data = {
            'artist_id': artist['id'],
            'artist_name': artist['name'],
            'popularity': artist['popularity'],
            'followers': artist['followers']['total']
        }

        artists_info.append(artist_data)

    return artists_info

def get_albums(token, artist_id):
    """
    Obtiene una lista de álbumes de un artista en especifico de la API de Spotify.
    """
    url = f"{os.getenv('API_SPOTIFY')}/artists/{artist_id}/albums"
    headers = get_auth_header(token)

    params = {
        'include_groups': 'album,single,compilation',
        'limit': 50
    }

    albums_info = []
    while url:
        result = get(url, headers=headers, params=params, timeout=600)  

        if result.status_code != 200:
            raise requests.exceptions.HTTPError(f"Error al obtener los álbumes. Código de estado: {result.status_code}")

        json_result = json.loads(result.content)

        for album in json_result['items']:
            album_details = get_album_details(album['id'], headers)
            cover_image = album['images'][0]['url'] if album['images'] else ''

            album_data = {
                'album_id': album['id'],
                'album_name': album['name'],
                'album_type': album['album_type'],
                'release_date': album['release_date'],
                'available_markets': album['available_markets'],
                'num_available_markets': len(album['available_markets']),
                'popularity': album_details['popularity'],
                'cover_image': cover_image,
                'upc': album_details['upc'],
                'copyright_c': album_details['copyright_c'],
                'copyright_p': album_details['copyright_p'],
                'artist_id': artist_id
            }

            albums_info.append(album_data)

        url = json_result['next']
        params = {}  # Clear params for the next requests as 'next' URL already includes them

    return albums_info

def get_album_details(album_id, headers):
    """
    Obtiene los detalles de un álbum en específico de la API de Spotify.
    """
    album_details_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}"

    album_details_result = get(album_details_url, headers=headers, timeout=300)

    album_details = json.loads(album_details_result.content)

    copyrights = album_details.get('copyrights', [])
    copyright_c = [c['text'] for c in copyrights if c['type'] == 'C']
    copyright_p = [c['text'] for c in copyrights if c['type'] == 'P']

    return {
        'upc': album_details.get('external_ids', {}).get('upc', 'Sin datos'),
        'popularity': album_details.get('popularity', 0),
        'copyright_c': copyright_c,
        'copyright_p': copyright_p,
    }


# def get_songs(token, artist_id):
#     """
#     Obtiene una lista de canciones de un artista en específico de la API de Spotify.
#     """
#     url = f"{os.getenv('API_SPOTIFY')}/artists/{artist_id}/albums"
#     headers = get_auth_header(token)
#     params = {'include_groups': 'album,single,compilation', 'limit': 50}

#     albums_result = requests.get(url, headers=headers, params=params)

#     if albums_result.status_code != 200:
#         raise requests.exceptions.HTTPError(f"Error al obtener las canciones. Código de estado: {albums_result.status_code}")

#     albums_json = albums_result.json() 
#     songs_info = []

#     for album in albums_json['items']:
#         album_id = album['id']
#         tracks_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}/tracks"
#         tracks_result = requests.get(tracks_url, headers=headers)
#         tracks_json = tracks_result.json()

#         for track in tracks_json['items']:
#             track_id = track['id']
#             track_details = get_track_details(token, track_id) 
#             isrc = track_details.get('external_ids', {}).get('isrc', 'Sin datos')
#             spotify_url = track_details['external_urls']['spotify']
#             song_links = get_song_links(spotify_url)

#             song_data = {
#                 'song_id': track_id,
#                 'song_name': track['name'],
#                 'interpreters_name': ", ".join([artist['name'] for artist in track['artists']]),
#                 'composers_name': 'N/A', # Spotify API does not provide composer information
#                 'producers_name': 'N/A', # Spotify API does not provide composer information
#                 'duration': track['duration_ms'],
#                 'release_date': album['release_date'],
#                 'isrc': isrc,
#                 'popularity': track_details['popularity'],
#                 'spotify_url': spotify_url,
#                 'itunes_link': song_links['itunes_link'] if song_links['itunes_link'] else 'Sin datos',
#                 'tidal_link': song_links['tidal_link'] if song_links['tidal_link'] else 'Sin datos',
#                 'amazon_link': song_links['amazon_link'] if song_links['amazon_link'] else 'Sin datos',
#                 'deezer_link': song_links['deezer_link'] if song_links['deezer_link'] else 'Sin datos',
#                 'youtube_link': song_links['youtube_link'] if song_links['youtube_link'] else 'Sin datos',
#                 'album_id': album_id
#             }
#             songs_info.append(song_data)

#     return songs_info

def get_songs_from_album(token, album_id):
    """
    Obtiene una lista de canciones de un álbum específico de la API de Spotify.
    """
    url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}/tracks"
    headers = get_auth_header(token)

    tracks_result = requests.get(url, headers=headers)

    if tracks_result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener las canciones. Código de estado: {tracks_result.status_code}")

    tracks_json = tracks_result.json()
    songs_info = []

    for track in tracks_json['items']:
        track_id = track['id']
        track_details = get_track_details(token, track_id) 
        isrc = track_details.get('external_ids', {}).get('isrc', 'Sin datos')
        spotify_url = track_details['external_urls']['spotify']
        song_links = get_song_links(spotify_url)
        song_name = track['name']
        artist_name = ", ".join([artist['name'] for artist in track['artists']])

        try:
            producers, writers = get_song_info_by_name_artist(song_name, artist_name)
        except ValueError as e:
            producers = ['Sin datos']
            writers = ['Sin datos']

        song_data = {
            'song_id': track_id,
            'song_name': track['name'],
            'interpreters_name': ", ".join([artist['name'] for artist in track['artists']]),
            'composers_name': ", ".join(writers), 
            'producers_name': ", ".join(producers), 
            'duration': track['duration_ms'],
            'release_date': track_details['album']['release_date'],
            'isrc': isrc,
            'popularity': track_details['popularity'],
            'spotify_url': spotify_url,
            'itunes_link': song_links['itunes_link'] if song_links['itunes_link'] else 'Sin datos',
            'tidal_link': song_links['tidal_link'] if song_links['tidal_link'] else 'Sin datos',
            'amazon_link': song_links['amazon_link'] if song_links['amazon_link'] else 'Sin datos',
            'deezer_link': song_links['deezer_link'] if song_links['deezer_link'] else 'Sin datos',
            'youtube_link': song_links['youtube_link'] if song_links['youtube_link'] else 'Sin datos',
            'album_id': album_id
        }
        songs_info.append(song_data)

    return songs_info

def get_track_details(token, track_id):
    """
    Obtiene los detalles de una canción en específico de la API de Spotify.
    """
    url = f"{os.getenv('API_SPOTIFY')}/tracks/{track_id}" 

    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los detalles de la canción. Código de estado: {response.status_code}")

    return response.json()