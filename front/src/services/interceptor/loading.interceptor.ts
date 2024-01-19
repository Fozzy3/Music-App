// loading.interceptor.ts

import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { LoadingService } from '../loading.service'; // Importa tu servicio de carga

@Injectable()
export class LoadingInterceptor implements HttpInterceptor {
  constructor(private loadingService: LoadingService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    this.loadingService.showLoading(); // Muestra el indicador de carga al inicio de la solicitud

    return next.handle(request).pipe(
      finalize(() => {
        this.loadingService.hideLoading(); // Oculta el indicador de carga al finalizar la solicitud
      })
    );
  }
}
