// loading.service.ts

import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoadingService {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();
  loadingText$ = new BehaviorSubject<string>('');

  showLoading(text: string = 'Cargando...') {
    this.loadingText$.next(text);
    this.loadingSubject.next(true);
  }

  hideLoading() {
    this.loadingText$.next('');
    this.loadingSubject.next(false);
  }
}
