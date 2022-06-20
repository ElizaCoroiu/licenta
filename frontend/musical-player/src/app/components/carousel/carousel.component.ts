import { AfterViewInit, Component, EventEmitter, OnDestroy, OnInit, Output } from '@angular/core';
import { RestApiService } from 'src/app/services/rest-api.service';
import { DomSanitizer } from '@angular/platform-browser';
import { combineLatest, map } from 'rxjs';
import { UploadService } from 'src/app/services/upload.service';

@Component({
  selector: 'app-carousel',
  templateUrl: './carousel.component.html',
  styleUrls: ['./carousel.component.scss']
})
export class CarouselComponent implements OnInit, AfterViewInit, OnDestroy {
  @Output() toggleChange: EventEmitter<any> = new EventEmitter();
  thumbnails: any = [];
  filePaths: any;
  files: any;

  constructor(public restApi: RestApiService, private sanitizer: DomSanitizer,
              public uploadService: UploadService) {}


  ngOnInit() {
    this.getFiles();
    this.toggleChange.emit("Carousel loaded");
  }

  ngAfterViewInit(): void {
    this.uploadService.newImage$.pipe().subscribe((data: any) => {
      this.thumbnails = [];
      this.getFiles();
    })
  }

  async getFiles() {
    this.filePaths = await this.restApi.getFilePaths().toPromise();

    this.filePaths.forEach((path: any) => {
      this.files = combineLatest({
        image: this.restApi.getFile(path),
        processedValues: this.restApi.getProcessedImage(path)
      })
      .pipe(
        map(response => {
          const image = response.image;
          const processedValues = response.processedValues;
          const picture = URL.createObjectURL(image);
          const thumbnail = this.sanitizer.bypassSecurityTrustUrl(picture);

          const result: any[] = [];
          result.push({thumbnail, processedValues})

          return result;
        })
      ).subscribe((data) => {
        this.thumbnails.push(data[0]);
      })
    })
  }

  ngOnDestroy(): void {
    this.uploadService.newImage$.unsubscribe();
    this.files.unsubscribe();
  }
}
