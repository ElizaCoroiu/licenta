import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { RestApiService } from 'src/app/services/rest-api.service';
import { UploadService } from 'src/app/services/upload.service';

@Component({
  selector: 'app-drag-and-drop',
  templateUrl: './drag-and-drop.component.html',
  styleUrls: ['./drag-and-drop.component.scss']
})
export class DragAndDropComponent implements OnInit {
  isVisible: boolean = false;
  title = 'dropzone';
  thumbnail: any

  constructor(public restApi: RestApiService, private sanitizer: DomSanitizer,
              public uploadService: UploadService) { }

  ngOnInit(): void {
  }

  onClick() {
    this.isVisible = !this.isVisible;
  }

  onSelect(event: any){
    const formData = new FormData();
    formData.append("file", event.addedFiles[0]);

    this.restApi.createFile(formData).subscribe(() => {
      this.uploadService.imageReceived();
    })
  }

  receive(event: any) {
    console.log(event)
  }
}
