import { AfterViewInit, Component, OnChanges, OnInit, ViewChild, ChangeDetectorRef } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { OutlierDetectionService } from '../services/outlier-detection/outlier-detection.service';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner'
import { SpinnerService } from '../spinner/spinner.service';
import { GraphComponent } from '../graph/graph.component';
import { MatDialog } from '@angular/material/dialog';
import { tap } from "rxjs/operators";

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

/**
 * @title Basic use of `<table mat-table>`
 */

 @Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss']
})

export class DataTableComponent implements OnInit, AfterViewInit{
  displayedColumns: string[] | undefined;
  indexValue: any = [];
  dataSource: any = [];
  showTable = false;
  activatedRow = null;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  showSpinner = false;
  countOfOutlier = null;
  id = '';
  constructor(public outlierDetectionService: OutlierDetectionService, 
    private SpinnerService: SpinnerService, 
    private cdRef: ChangeDetectorRef,
    public dialog: MatDialog
    ) { 
      
    }
    //this.init();


  ngOnInit() {
    this.SpinnerService.getSpinnerObserver().subscribe((status) =>{
      this.showSpinner = status === 'start';
      this.cdRef.detectChanges();
    });

    this.outlierDetectionService.dataWithOutlierEvent.subscribe((data: any) => {
      console.log(data);
      this.countOfOutlier = data.reduce((acc: any, cur: any) => cur.Outlier === true ? ++acc : acc, 0);
      
      this.displayedColumns = Object.keys(data[0]);
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.paginator = this.paginator;
      this.SpinnerService.requestEnded();
      this.showTable = true;
      //console.log(this.displayedColumns)
    })
  }

  ngAfterViewInit() {
    //Assigning original paginator!
    this.dataSource.paginator = this.paginator; 
  }

  showGraph(id: number, KPI: any) {
    this.outlierDetectionService.getKpiDataById(id).subscribe(data => this.id = data.id);
    //this.outlierDetectionService.getEstimatedDataById(id).subscribe(data => this.id = data.id);
    const dialogRef = this.dialog.open(GraphComponent, {
      width: '1250px',
      data: {id: id, KPI}
    
    });
    dialogRef.afterClosed().pipe(
      tap(() => this.activatedRow = null)
    );
  }
  

}

