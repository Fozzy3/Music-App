import base64
import json
from dotenv import load_dotenv
import os
from requests import post, get
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def get_upc_from_album_details(album_id, headers):
    album_details_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}"
    album_details_result = get(album_details_url, headers=headers)
    album_details = json.loads(album_details_result.content)
    return album_details.get('external_ids', {}).get('upc', 'N/A')
    
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers ={
        "Authorization": "Basic " + auth_base64,  
        "Content-Type": "application/x-www-form-urlencoded"  
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    if token is not None:
      return token
    else:
      print("Error al obtener el access_token. Respuesta recibida:")
      print(json_result)
      return None

def search_for_artist(token, artist_name):
    url = f"{os.getenv('API_SPOTIFY')}/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result)==0:
        print("NO HAY ARTISTA CON ESE NOMBRE")
        return None
    
    return json_result[0]

def get_albums(token, artist_id):
    url = f"{os.getenv('API_SPOTIFY')}/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    params = {
        'include_groups': 'album,single,compilation',
        'limit': 50
    }
    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)

    albums_info = []

    for album in json_result['items']:
        upc = get_upc_from_album_details(album['id'], headers)

        copyrights = [c['text'].split(" (C)")[0] for c in album.get('copyrights', []) if "(C)" in c['text']]

        album_data = {
            'name': album['name'],
            'release_date': album['release_date'],
            'album_type': album['album_type'],
            'available_markets': len(album['available_markets']),
            'copyright_holders': copyrights,
            'upc': upc  
        }

        albums_info.append(album_data)

    return albums_info

def get_songs(token, artist_id):
    url = f"{os.getenv('API_SPOTIFY')}/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    params = {'include_groups': 'album,single,compilation', 'limit': 50}
    albums_result = get(url, headers=headers, params=params)
    albums_json = json.loads(albums_result.content)
    songs_info = []
    for album in albums_json['items']:
        album_id = album['id']
        album_upc = album.get('external_ids', {}).get('upc', 'N/A')

        tracks_url = f"{os.getenv('API_SPOTIFY')}/albums/{album_id}/tracks"
        tracks_result = get(tracks_url, headers=headers)
        tracks_json = json.loads(tracks_result.content)

        for track in tracks_json['items']:
            track_id = track['id']
            track_details = get_track_details(token, track_id) 
            isrc = track_details.get('external_ids', {}).get('isrc', 'N/A')
            song_data = {
                'song_name': track['name'],
                'artists': ", ".join([artist['name'] for artist in track['artists']]),
                'isrc': isrc,
                'upc': album_upc,
                'duration_ms': track['duration_ms'],
                'release_year': album['release_date'][:4],
                'song_link': track['external_urls']['spotify']
            }
            songs_info.append(song_data)
    return songs_info

def get_track_details(token, track_id):
    url = f"{os.getenv('API_SPOTIFY')}/tracks/{track_id}"    
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def save_spotify_data_to_db(artist_name, data):
#     db = SessionLocal()
#     db_spotify_data = SpotifyData(artist_name=artist_name, data=data)
#     db.add(db_spotify_data)
#     db.commit()
#     db.refresh(db_spotify_data)

def get_spotify_data(artist_name):
    try:
        token = get_token()
        result = search_for_artist(token, artist_name)
        if not result:
            return {"error": f"No se encontró el artista con el nombre {artist_name}"}

        artist_id = result["id"]
        albums = get_albums(token, artist_id)
        albums_info = []

        for idx, album in enumerate(albums):
            album_data = {
                'index': idx + 1,
                'name': album['name'],
                'release_date': album['release_date'],
                'album_type': album['album_type'],
                'available_markets': album['available_markets'],
                'copyright_holders': album['copyright_holders'],
                'upc': album['upc']
            }
            albums_info.append(album_data)

        # Guarda los resultados en la base de datos
        # save_spotify_data_to_db(artist_name, {"artist_info": result, "albums": albums_info})

        return {"artist_info": result, "albums": albums_info}
    except Exception as e:
        return {"error": str(e)}