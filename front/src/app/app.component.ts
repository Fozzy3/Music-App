import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { LayoutComponent } from './layout/layout.component';
import { LoadingService } from '../services/loading.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, LayoutComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'front';

  isLoading: boolean = false;

  constructor(private loadingService: LoadingService) {}

  ngOnInit() {
    this.loadingService.loading$.subscribe((loading) => {
      this.isLoading = loading;
    });

    this.loadingService.loading$.subscribe((loading) => {
      this.isLoading = loading;
    });
  }

}
