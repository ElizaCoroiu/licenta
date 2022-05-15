import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RestApiService } from 'src/app/services/rest-api.service';

@Component({
  selector: 'app-drag-and-drop',
  templateUrl: './drag-and-drop.component.html',
  styleUrls: ['./drag-and-drop.component.scss']
})
export class DragAndDropComponent implements OnInit {
  isVisible: boolean = false;
  title = 'dropzone';


  constructor(public restApi: RestApiService) { }

  ngOnInit(): void {
  }

  onClick() {
    this.isVisible = true;
  }

  onSelect(event: any){
    const formData = new FormData();
    formData.append("file", event.addedFiles[0]);
    
    this.restApi.createFile(formData).subscribe((data: {}) => {
      console.log(data);
    })
  }
}
