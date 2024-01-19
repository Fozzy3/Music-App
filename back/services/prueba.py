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

    result = get(url, headers=headers, params=params)  # Add timeout argument

    if result.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error al obtener los álbumes. Código de estado: {result.status_code}")

    json_result = json.loads(result.content)
    albums_info = []

    for album in json_result['items']:
        album_details = get_album_details(album['id'], headers)
        cover_image = album['images'][0]['url'] if album['images'] else None

        album_data = {
            'album_id': album['id'],
            'album_name': album['name'],
            'album_type': album['album_type'],
            'release_date': album['release_date'],
            'available_markets': album['available_markets'],
            'num_available_markets': len(album['available_markets']),
            'genres': album_details['genres'],
            'popularity': album_details['popularity'],
            'cover_image': cover_image,
            'upc': album_details['upc'],
            'copyright_c': album_details['copyright_c'],
            'copyright_p': album_details['copyright_p'],
            'artist_id': artist_id
        }

        albums_info.append(album_data)
    print("fase1albu",albums_info)

    return albums_info

def get_album_details(album_id, headers):
    """
    Obtiene los detalles de un álbum en específico de la API de Spotify.
    """
    album_details_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}"

    album_details_result = get(album_details_url, headers=headers, timeout=120)

    album_details = json.loads(album_details_result.content)

    copyrights = album_details.get('copyrights', [])
    copyright_c = [c['text'] for c in copyrights if c['type'] == 'C']
    copyright_p = [c['text'] for c in copyrights if c['type'] == 'P']

    return {
        'upc': album_details.get('external_ids', {}).get('upc', 'N/A'),
        'genres': album_details.get('genres', []),
        'popularity': album_details.get('popularity', 0),
        'copyright_c': copyright_c,
        'copyright_p': copyright_p,
    }



# Obtén el token de acceso
token = get_token()

artist_id = "1McMsnEElThX1knmY4oliG" # Asume que el artista fue encontrado

# Obtén los álbumes del artista
albums_info = get_albums(token, artist_id)

print("                             Imprimir2                                     ")
# Imprime los álbumes en la consola
for album in albums_info:
    print(album)
    

def get_album_data(artist_id):
        try:
                # Obtén el token
                token = get_token()
                                
                # Llama a la función get_albums
                albums = get_albums(token, artist_id)
                album_info = []
                print("fase1albu",albums)
                                
                for album in albums:
                        album_data = {
                                'album_id': album['album_id'],
                                'album_name': album['album_name'],
                                'album_type': album['album_type'],
                                'release_date': album['release_date'],
                                'available_markets': album['available_markets'],
                                'num_available_markets': album['num_available_markets'],
                                'popularity': album['popularity'],
                                'cover_image': album['cover_image'],
                                'upc': album['upc'],
                                'copyright_c': album['copyright_c'],
                                'copyright_p': album['copyright_p'],
                                'artist_id': album['artist_id']
                        }
                        album_info.append(album_data)

                return album_info
        except Exception as e:
                return {
                        "album": [{
                        'album_id': None,
                        'album_name': None,
                        'album_type': None,
                        'release_date': None,
                        'available_markets': None,
                        'num_available_markets': None,
                        'popularity': None,
                        'cover_image': None,
                        'upc': None,
                        'copyright_c': None,
                        'copyright_p': None,
                        'artist_id': None,
                        'error': str(e)
                }]
                }