import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RestApiService {
  apiURL = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'multipart/form-data',
    }),
  };

  createFile(file: any): Observable<any> {
    return this.http
      .post(
        this.apiURL + '/file', file
      )
      .pipe(retry(1), catchError(this.handleError));
  }

  getFile(filePath: string): Observable<any> {
    return this.http
      .get(this.apiURL + '/image/' + filePath, {responseType: 'blob'}
      )
      .pipe(retry(1), catchError(this.handleError));
  }

  getFilePaths(): Observable<any> {
    return this.http
      .get(this.apiURL + '/filepaths')
      .pipe(retry(1), catchError(this.handleError));
  }

  getProcessedImage(fileName: string): Observable<any> {
    return this.http
      .get(this.apiURL + '/processed_image/' + fileName)
      .pipe(retry(1), catchError(this.handleError));
  }

  handleError(error: any) {
    let errorMessage = '';
    if (error.error instanceof ErrorEvent) {
      errorMessage = error.error.message;
    } else {
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    window.alert(errorMessage);
    return throwError(() => {
      return errorMessage;
    });
  }
}
