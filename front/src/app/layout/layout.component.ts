import { Component } from '@angular/core';
import { ConnectionService } from '../../services/connection.service';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [TableModule, ButtonModule],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss'
})
export class LayoutComponent {

  customers: any = [
    {
      id: 1000,
      name: 'James Butt',
      country: {
          name: 'Algeria',
          code: 'dz'
      },
      company: 'Benton, John B Jr',
      date: '2015-09-13',
      status: 'unqualified',
      verified: true,
      activity: 17,
      representative: {
          name: 'Ioni Bowcher',
          image: 'ionibowcher.png'
      },
      balance: 70663
  },
  {
    id: 1000,
    name: 'James Butt',
    country: {
        name: 'Algeria',
        code: 'dz'
    },
    company: 'Benton, John B Jr',
    date: '2015-09-13',
    status: 'unqualified',
    verified: true,
    activity: 17,
    representative: {
        name: 'Ioni Bowcher',
        image: 'ionibowcher.png'
    },
    balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
},
{
  id: 1000,
  name: 'James Butt',
  country: {
      name: 'Algeria',
      code: 'dz'
  },
  company: 'Benton, John B Jr',
  date: '2015-09-13',
  status: 'unqualified',
  verified: true,
  activity: 17,
  representative: {
      name: 'Ioni Bowcher',
      image: 'ionibowcher.png'
  },
  balance: 70663
}

  ]

  constructor(private connService: ConnectionService){}

  ngOnInit(){

    this.connService.getData().subscribe({
      next: (response) => {
          console.log(response)
      },
    })
  }
}
