import { Component } from '@angular/core';
import { ConnectionService } from '../../services/connection.service';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { MenubarModule } from 'primeng/menubar';
import { InputTextModule } from 'primeng/inputtext';
import { FormsModule } from '@angular/forms';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ToastModule } from 'primeng/toast';
import { ConfirmationService, MessageService } from 'primeng/api';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [
    TableModule,
    ButtonModule,
    MenubarModule,
    InputTextModule,
    FormsModule,
    ConfirmDialogModule,
    ToastModule,
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss',
})
export class LayoutComponent {
  items: any[] = [
    {
      label: 'File',
      icon: 'pi pi-fw pi-file',
    },
    {
      label: 'Edit',
      icon: 'pi pi-fw pi-pencil',
    },
    {
      label: 'Users',
      icon: 'pi pi-fw pi-user',
    },
    {
      label: 'Events',
      icon: 'pi pi-fw pi-calendar',
    },
    {
      label: 'Quit',
      icon: 'pi pi-fw pi-power-off',
    },
  ];

  artist: any = null;
  artistData: any = null;
  albumData: any = null;
  songsData: any = null;

  constructor(
    private connService: ConnectionService,
    private confirmationService: ConfirmationService,
    private messageService: MessageService
  ) {}

  ngOnInit() {}

  clear(){
    this.artist = null;
    this.artistData = null;
    this.albumData = null;
    this.songsData = null;
  }
  searchArt(event: Event) {
    this.confirmationService.confirm({
      target: event.target as EventTarget,
      message: 'Esta seguro del artista a buscar?',
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      acceptIcon: 'none',
      rejectIcon: 'none',
      rejectButtonStyleClass: 'p-button-text',
      accept: () => {
        if (this.artist) {
          this.searchArtist();
        } else {
          this.messageService.add({
            severity: 'error',
            summary: 'El campo no puede estar vació',
            detail: 'Por favor ingrese un artista',
          });
        }
      },
      reject: () => {},
    });
  }

  searchArtist() {
    this.connService.getArtist(this.artist).subscribe({
      next: (response) => {
        if (response) {
          this.messageService.add({
            severity: 'success',
            summary: 'Artista encontrado',
            detail: '',
          });
          this.artistData = response;
        } else {
          this.messageService.add({
            severity: 'error',
            summary: 'Artista no encontrado',
            detail: 'Pruebe con otro nombre',
          });
        }
      },
    });
  }

  searchAlbum(id: any) {
    this.connService.getAlbum(id).subscribe({
      next: (response) => {
        if (response) {
          this.messageService.add({
            severity: 'success',
            summary: 'Artista encontrado',
            detail: '',
          });
          this.albumData = response;
        } else {
          this.messageService.add({
            severity: 'error',
            summary: 'Artista no encontrado',
            detail: 'Pruebe con otro nombre',
          });
        }
      },
    });
  }

  searchSong(id: any) {
    this.connService.getSongs(id).subscribe({
      next: (response) => {
        if (response) {
          this.messageService.add({
            severity: 'success',
            summary: 'Artista encontrado',
            detail: '',
          });
          this.songsData = response;
        } else {
          this.messageService.add({
            severity: 'error',
            summary: 'Artista no encontrado',
            detail: 'Pruebe con otro nombre',
          });
        }
      },
    });
  }

  search(event: Event, id: String, type: String) {
    this.confirmationService.confirm({
      target: event.target as EventTarget,
      message: `Esta seguro de buscar ${type} del artista?, puede tardar un poco`,
      header: 'Confirmación',
      icon: 'pi pi-exclamation-triangle',
      acceptIcon: 'none',
      rejectIcon: 'none',
      rejectButtonStyleClass: 'p-button-text',
      accept: () => {
        if (this.artist) {
          if(type == "álbumes"){
            this.searchAlbum(id);
          }else if(type == "canciones"){
            this.searchSong(id);
          }
        }
      },
      reject: () => {},
    });
  }

}
