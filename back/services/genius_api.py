import requests
import aiohttp

# Define las credenciales de la API
CLIENT_ACCESS_TOKEN = 'vLnNFS2n6OB0nh52yOeXlFavwNncl4dYx8Ea9zCeJJ6v-O99AdgP6wA4ptt-CwBA'

def get_song_info(song_id):
    url = f"https://api.genius.com/songs/{song_id}"
    headers = {"Authorization": f"Bearer {CLIENT_ACCESS_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        song_info = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al hacer la solicitud: {e}")

    song_info = song_info["response"]["song"]
    producers = [producer["name"] for producer in song_info["producer_artists"]] if song_info["producer_artists"] else ["Sin datos"]
    writers = [writer["name"] for writer in song_info["writer_artists"]] if song_info["writer_artists"] else ["Sin datos"]
    return producers, writers

def search_song_artist_partial_match(song_name, artist_name):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {CLIENT_ACCESS_TOKEN}"}
    params = {"q": f"{song_name} {artist_name}"}
    try:
        response = requests.get(url, headers=headers, params=params)  
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al hacer la solicitud: {e}")

    results = response.json()["response"]["hits"]
    for result in results:
        if song_name.lower() in result["result"]["title"].lower() and artist_name.lower() in result["result"]["primary_artist"]["name"].lower():
            return result["result"]["id"]
    return None

def get_song_info_by_name_artist(song_name, artist_name):
    song_id = search_song_artist_partial_match(song_name, artist_name)
    if song_id is not None:
        return get_song_info(song_id)
    else:
        raise ValueError(f"No se encontró la canción: {song_name} por el artista: {artist_name}")

