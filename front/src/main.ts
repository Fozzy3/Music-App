import { bootstrapApplication } from '@angular/platform-browser';
import  preview  from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, preview.decorators)
  .catch((err) => console.error(err));
