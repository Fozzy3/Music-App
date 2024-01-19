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





def get_songs(token, artist_id):
    """
    Obtiene una lista de canciones de un artista en específico de la API de Spotify.
    """
    url = f"{os.getenv('API_SPOTIFY')}/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    params = {'include_groups': 'album,single,compilation', 'limit': 50}

    albums_result = requests.get(url, headers=headers, params=params)

    if albums_result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener las canciones. Código de estado: {albums_result.status_code}")

    albums_json = albums_result.json() 
    songs_info = []

    for album in albums_json['items']:
        album_id = album['id']
        tracks_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}/tracks"
        tracks_result = requests.get(tracks_url, headers=headers)
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

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los detalles de la canción. Código de estado: {response.status_code}")

    return response.json()



# Obtén el token de acceso
token = get_token()

artist_id = "1McMsnEElThX1knmY4oliG" # Asume que el artista fue encontrado

# Obtén los álbumes del artista
songs_info = get_songs(token, artist_id)

print("                             Imprimir                                     ")
# Imprime los álbumes en la consola
for i, song in enumerate(songs_info, start=1):
    print(f"{i}: {song}")
