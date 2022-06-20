import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  newImage: any = new Subject<string>()
  newImage$: any = this.newImage.asObservable()

  constructor() { }

  imageReceived() {
    this.newImage.next("Image send")
  }
}
