import base64
import json
from dotenv import load_dotenv
import os
from requests import post, get
import requests
from services.song_links import get_song_links


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_auth_header(token):
    """
    Diccionario usado como cabecera para las solicitudes autenticadas a la API.
    """
    return{"Authorization": "Bearer " + token}

def get_token():
    """
    Obtención token de acceso de la API de Spotify.
    El token de acceso es necesario para hacer solicitudes autenticadas a la API de Spotify.
    """

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,  
        "Content-Type": "application/x-www-form-urlencoded"  
    }
    data = {"grant_type" : "client_credentials"}

    result = post(url, headers=headers, data=data, timeout=120)

    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener el access_token. Código de estado: {result.status_code}")

    json_result = json.loads(result.content)
    token = json_result.get("access_token")

    if token is None:
        raise ValueError("Error al obtener el access_token. No se encontró el token en la respuesta.")

    return token


def get_artist(token, artist_name):
    """
    Busqueda información sobre el artista especificado.
    """
    url = f"{os.getenv('API_SPOTIFY')}/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers, timeout=120)  

    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener el artista. Código de estado: {result.status_code}")

    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result)==0:
        raise ValueError("No se encontró ningún artista con ese nombre.")
    
    artist = json_result[0]
    artist_info = []

    artist_data = {
        'artist_id': artist['id'],
        'artist_name': artist['name'],
        'popularity': artist['popularity'],
        'followers': artist['followers']['total']
    }

    artist_info.append(artist_data)

    return artist_info

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

    result = get(url, headers=headers, params=params, timeout=120)  # Add timeout argument

    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los álbumes. Código de estado: {result.status_code}")

    json_result = json.loads(result.content)
    albums_info = []

    for album in json_result['items']:
        upc = get_upc_from_album_details(album['id'], headers)
        cover_image = album['images'][0]['url'] if album['images'] else None

        copyrights_c = [c['text'].split(" (C)")[0] for c in album.get('copyrights', []) if "(C)" in c['text']]
        copyrights_p = [c['text'].split(" (P)")[0] for c in album.get('copyrights', []) if "(P)" in c['text']]

        album_data = {
            'album_id': album['id'],
            'album_name': album['name'],
            'album_type': album['album_type'],
            'release_date': album['release_date'],
            'available_markets': album['available_markets'],
            'num_available_markets': len(album['available_markets']),
            'genres': album.get('genres', []),  
            'popularity': album['popularity'],
            'cover_image': cover_image,
            'upc': upc,
            'copyright_c': copyrights_c,
            'copyright_p': copyrights_p,
            'artist_id': artist_id
        }

        albums_info.append(album_data)

    return albums_info

def get_upc_from_album_details(album_id, headers):
    """
    Obtiene el código UPC de los detalles de un álbum en específico de la API de Spotify.
    """
    album_details_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}"

    album_details_result = get(album_details_url, headers=headers, timeout=120)

    album_details = json.loads(album_details_result.content)

    return album_details.get('external_ids', {}).get('upc', 'N/A')


def get_songs(token, artist_id):
    """
    Obtiene una lista de canciones de un artista en específico de la API de Spotify.
    """
    url = f"{os.getenv('API_SPOTIFY')}/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    params = {'include_groups': 'album,single,compilation', 'limit': 50}

    albums_result = requests.get(url, headers=headers, params=params, timeout=120)

    if albums_result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener las canciones. Código de estado: {albums_result.status_code}")

    albums_json = albums_result.json() 
    songs_info = []

    for album in albums_json['items']:
        album_id = album['id']
        tracks_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}/tracks"
        tracks_result = requests.get(tracks_url, headers=headers, timeout=120)
        tracks_json = tracks_result.json()

        for track in tracks_json['items']:
            track_id = track['id']
            track_details = get_track_details(token, track_id) 
            isrc = track_details.get('external_ids', {}).get('isrc', 'N/A')
            spotify_url = track_details['external_urls']['spotify']
            song_links = get_song_links(spotify_url)

            song_data = {
                'song_id': track_id,
                'song_name': track['name'],
                'interpreters_name': ", ".join([artist['name'] for artist in track['artists']]),
                'composers_name': 'N/A', # Spotify API does not provide composer information
                'producers_name': 'N/A', # Spotify API does not provide composer information
                'duration': track['duration_ms'],
                'release_year': album['release_date'][:4],
                'isrc': isrc,
                'popularity': track_details['popularity'],
                'spotify_url': spotify_url,
                'itunes_link': song_links.get('itunes_link'),
                'tidal_link': song_links.get('tidal_link'),
                'amazon_link': song_links.get('amazon_link'),
                'deezer_link': song_links.get('deezer_link'),
                'youtube_link': song_links.get('youtube_link'),
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

    response = requests.get(url, headers=headers, timeout=120)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los detalles de la canción. Código de estado: {response.status_code}")

    return response.json()