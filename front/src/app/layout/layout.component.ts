import { Component } from '@angular/core';
import { ConnectionService } from '../services/connection.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent {


  constructor(private connService: ConnectionService){}

  ngOnInit(){
    this.connService.getData().subscribe({
      next: (response) => {
        console.log(response)
      }
    })
  }
}
