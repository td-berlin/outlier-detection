import { HttpClient, HttpEventType } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { OutlierDetectionService } from '../services/outlier-detection/outlier-detection.service';
import { SpinnerService } from '../spinner/spinner.service';

@Component({
  selector: 'app-input-form',
  templateUrl: './input-form.component.html',
  styleUrls: ['./input-form.component.scss']
})
export class InputFormComponent implements OnInit {
  formUploadData: any;
  graphForm = new FormGroup({

  });
  constructor(private outlierDetectionService: OutlierDetectionService,
              private spinnerService: SpinnerService) { }

  ngOnInit(): void {

  }

  onFileSelected(event: any) {
    //console.log(event)
    const file: File = event.target.files[0];

    if (file) {
      this.formUploadData = new FormData();
      this.formUploadData.append("file", file);
    }
  }

  uploadFile(): void {
    this.spinnerService.requestStarted();
    this.outlierDetectionService.uploadFile(this.formUploadData).subscribe((data: any) => {
      this.outlierDetectionService.dataWithOutlierEvent.emit(data.dataWithOutlier);
    }, err => {
      console.log(err)
    })
  }
}


