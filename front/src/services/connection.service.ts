import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/enviorment';
import { HttpClientModule } from '@angular/common/http';


const options = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
};

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  constructor(private http: HttpClient, public httpClient: HttpClientModule) { }


  getArtist(artist_name: any, select_market:any){
    return select_market
    ?  this.http.get(`${environment.API_URL}/spotify_artists/${artist_name}?market=${select_market}`)
    : this.http.get(`${environment.API_URL}/spotify_artists/${artist_name}`);
  }

  getAlbum(id_artist: any){
    return this.http.get(`${environment.API_URL}/spotify_albums/${id_artist}`);
  }

  getSongs(id_album: any){
    return this.http.get(`${environment.API_URL}/spotify_songs/${id_album}`);
  }

  postSaveArtist(id_album: any){
    return this.http.post(`${environment.API_URL}/save_artist_data`, id_album);
  }


  postSaveAlbum(albums_data: any){
    console.log(albums_data)
    return this.http.post(`${environment.API_URL}/save_album_data`, albums_data);
  }



}




