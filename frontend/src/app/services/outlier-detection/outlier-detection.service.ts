import { HttpClient, HttpHeaders  } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class OutlierDetectionService {

  dataWithOutlierEvent:  EventEmitter<any> = new EventEmitter();

  constructor(private http: HttpClient) { }



  upload(): Observable<any> {
    return this.http.get('http://127.0.0.1:5000/')
  }

  uploadFile(file: File): Observable<any> {
    return this.http.post('http://127.0.0.1:5000/upload-file', file)
  }

  getKpiDataById(id: any): Observable<any> {
    return this.http.get('http://127.0.0.1:5000/show_graph?id='+id)
    
  }

}
