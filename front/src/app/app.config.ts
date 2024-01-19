import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { LoadingInterceptor } from '../services/interceptor/loading.interceptor';
import { ConfirmationService, MessageService } from 'primeng/api';

const decorators: ApplicationConfig = {
  providers: [provideRouter(routes), importProvidersFrom(HttpClientModule), importProvidersFrom(BrowserModule), importProvidersFrom(BrowserAnimationsModule),     {
    provide: HTTP_INTERCEPTORS,
    useClass: LoadingInterceptor,
    multi: true,
  },ConfirmationService, MessageService]
};

const appConfig = {
  decorators: decorators
};
export default appConfig;
