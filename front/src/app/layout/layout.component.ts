import { Component } from '@angular/core';
import { ConnectionService } from '../../services/connection.service';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { MenubarModule } from 'primeng/menubar';
import { InputTextModule } from 'primeng/inputtext';
import { FormsModule } from '@angular/forms';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ToastModule } from 'primeng/toast';
import { CommonModule } from '@angular/common';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DialogModule } from 'primeng/dialog';
import { markets } from '../core/markets.class';
import { DropdownModule } from 'primeng/dropdown';

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
    CommonModule,
    DialogModule,
    DropdownModule
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
  selectMarket: any = null;
  selectedAlbums: any = null;
  markets: any[]|undefined;
  constructor(
    private connService: ConnectionService,
    private confirmationService: ConfirmationService,
    private messageService: MessageService,
  ) {}

  ngOnInit() {
    this.markets = markets;
    }

  clear(){
    this.artist = null;
    this.artistData = null;
    this.albumData = null;
    this.songsData = null;
    this.selectMarket = null;
  }

  searchArtist() {
    this.selectedAlbums = null;
    this.connService.getArtist(this.artist, this.selectMarket).subscribe({
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
          this.showDialog();
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

  visible: boolean = false;

  showDialog() {
      this.visible = true;
  }

  albumSelect: any = null;

  search(event: Event, id: String, album_title: String,type: String) {
    this.albumSelect = album_title;
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


  saveArtist(artist: any){
    this.connService.postSaveArtist(artist).subscribe({
      next: (response) => {
        if (response) {
          this.messageService.add({
            severity: 'success',
            summary: 'Artista guardado',
            detail: 'El artista de guardo en la BD local correctamente',
          });
        } else {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'No se pudo guardar',
          });
        }
      },
    });
  }


  questAlbum(event: Event) {
    this.confirmationService.confirm({
      target: event.target as EventTarget,
      message: `Esta seguro de guardar dichos álbumes en la BD?`,
      header: 'Confirmación',
      icon: 'pi pi-exclamation-triangle',
      acceptIcon: 'none',
      rejectIcon: 'none',
      rejectButtonStyleClass: 'p-button-text',
      accept: () => {
        this.saveAlbums()
      },
      reject: () => {},
    });
  }


  saveAlbums(){
    this.connService.postSaveAlbum(this.selectedAlbums).subscribe({
      next: (response) => {
        if (response) {
          this.messageService.add({
            severity: 'success',
            summary: 'Album guardado',
            detail: 'El album de guardo en la BD local correctamente',
          });
          this.selectedAlbums = null;
        } else {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'No se pudo guardar',
          });
        }
      },
    });

  }

}
