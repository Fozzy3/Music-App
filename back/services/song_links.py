import requests

def get_song_links(spotify_url):
    """
    Toma una URL de Spotify como argumento, realiza una solicitud a la API Songlink,
    devuelve un diccionario con los enlaces de canciones de diferentes plataformas
    """
    api_url = f"https://api.song.link/v1-alpha.1/links?url={spotify_url}"
    try:
        response = requests.get(api_url, timeout=300)
        response.raise_for_status()  # Lanza una excepción si la respuesta contiene un código de estado HTTP de error
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return None

    song_links = response.json()
    if 'linksByPlatform' in song_links:
        platforms = song_links['linksByPlatform']
        return {
            'itunes_link': platforms.get('itunes', {}).get('url'),
            'tidal_link': platforms.get('tidal', {}).get('url'),
            'amazon_link': platforms.get('amazonMusic', {}).get('url'),
            'deezer_link': platforms.get('deezer', {}).get('url'),
            'youtube_link': platforms.get('youtube', {}).get('url'),
        }
    else:
        print("La respuesta no contiene la clave 'linksByPlatform'")
        return None