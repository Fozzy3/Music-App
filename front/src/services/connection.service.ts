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


  getData(){
    return this.http.get(`${environment.API_URL}/users`);
  }
}




