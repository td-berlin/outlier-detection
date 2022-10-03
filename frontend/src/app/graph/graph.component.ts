import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { Subscription } from 'rxjs';
import { OutlierDetectionService } from '../services/outlier-detection/outlier-detection.service';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})

export class GraphComponent implements OnInit, OnDestroy {
  options: any;
  someSubscription: any;
  date : any[] = [];
  //date1 : any[] = [37];
  actualValue : any[] = [];
  estimatedValue : any[] = [];
  upperThreshold : any[] = [];
  outlierDate : any[] = [];
  outlierValue : any[] = [];
  outlierIndex : any[] = [];
  echartsIntance : any;
  lowerThreshold: any[] = [];


  outlierDetectionServiceSubscription: Subscription | undefined;
  router: any;
  constructor( private outlierDetectionService: OutlierDetectionService,
    public dialogRef: MatDialogRef<GraphComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }


  ngOnInit(): void {
    this.outlierDetectionServiceSubscription = this.outlierDetectionService.getKpiDataById(this.data.id).subscribe((data:any)=>{
      console.log(data)
       Object.entries(data.dataWithValue). 
       forEach(
        ([key, value]) => {
          this.date.push(String(key))
          this.actualValue.push(String(value))
        }
      );
      //for(var a of data.dataWithEstimate) {
       // this.estimatedValue.push(String(a))
        //}

      Object.entries(data.outlier). 
       forEach(
        ([key, value]) => {
          this.outlierDate.push(String(key))
          this.outlierValue.push(String(value))
        }
      );
      for(var a of data.outlierIndex) {
        if(a !== null && a !== undefined){
          this.outlierIndex.push(String(a))
        //console.log(this.outlierIndex.push(String(a)))
        }
        
      }
      for(var a of data?.lowerThreshold) {
        if(a !== null && a !== undefined){
          this.lowerThreshold.push(String(a))
        //console.log(this.outlierIndex.push(String(a)))
        }
      }
      for(var a of data?.upperThreshold) {
        this.upperThreshold.push(String(a))
      }
      this.options = data.upperThreshold.length == 1 ? this.setOptionsForMarkline(this.date, this.actualValue,  
      data.outlier, this.outlierIndex, this.lowerThreshold, this.upperThreshold) :
      this.setOptions(this.date, this.actualValue,  
      this.outlierDate, this.outlierValue, this.outlierIndex, this.lowerThreshold, this.upperThreshold)
    })
  }
  

  setOptions(date: any, actualValue: any, outlierDate: any, 
    outlierValue: any, outlierIndex: any, lowerThreshold: any, upperThreshold: any){
    return {
      title: {
        text: this.data.KPI,
      },
      legend: {
        //data: ['Actual Value', 'Estimated Value'],
        align: 'right'
      },
      tooltip: {
        show: true,
        trigger: "axis",
        triggerOn: "click",
      },
      xAxis: {
        data: date,
        silent: false,
        splitLine: {
          show: false,
        },
        color: 'black',
      },

      yAxis: {},
        dataZoom: [
          {
            type: 'inside',
            //throttle: 50
          }
        ],
        
      series: [
        {
          name: 'Actual Value',
          data: actualValue,
          type: 'line',
          showSymbol: false,
          markPoint: {
            symbol: outlierValue.length > 0 ? 'pin':'none',
            large:false,
            data: [{ name: 'Outlier', xAxis: outlierDate[0], yAxis: outlierValue[0]}],
            itemStyle: {
              color: 'red',
              opacity: 0.75
            }
          },

        },
        // {
        //   name: 'Estimated Value',
        //   data: estimatedValue,
        //   type: "line",
        //   showSymbol: false,
        // },
        {
          name: 'Lower Threshold',
          data: lowerThreshold,
          type: "line",
          showSymbol: false,
          color: 'rgb(19, 143, 114)',
          areaStyle: {
            color:'white',
            opacity:1.0,
            origin: "start",
        },
        },
        {
          name: 'Upper Threshold',
          data: upperThreshold,
          type: "line",
          showSymbol: false,
          z: -1,
          color: 'rgb(101, 214, 131)',
          areaStyle: {
            color:'green',
            opacity: 0.25
            //origin: "start",
        },
        }
      ],
    };
  }

  setOptionsForMarkline(date: any, actualValue: any, outlier: any, 
     outlierIndex: any, lowerThreshold: any, upperThreshold: any){
      console.log(outlier);
    return {
      title: {
        text: this.data.KPI,
      },
      legend: {
        align: 'right'
      },
      tooltip: {
        show: true,
        trigger: "axis",
        triggerOn: "click",
      },
      xAxis: {
        data: date,
        silent: false,
        splitLine: {
          show: false,
        },
        color: 'black',
      },

      yAxis: {},
        dataZoom: [
          {
            type: 'inside',
            //throttle: 50
          }
        ],
        
      series: [
        {
          name: 'Actual Value',
          data: actualValue,
          type: 'line',
          showSymbol: false,
          markPoint: {
            symbol: outlierIndex.length > 0?'pin':'none',
            large:false,
            data: this.getMarkPointData(outlier),
            itemStyle: {
              color: 'red',
              opacity: 0.75
            }
          },
          markLine: {
            data: [{
              symbol: "none",
              name: 'upperThreshold',
              yAxis: upperThreshold,
              label: {
                normal: {
                  show: true,
                  //position: 'insideEndTop'
                }
              },
              lineStyle: {
                normal: {
                  color: 'rgb(101, 214, 131)',
                  width: 1.5
                }
              }
            }]
          },
          
        }
      ],
    };
  }

  getMarkPointData(outlierValue: any): any{
    let markpointValues: { name: string; xAxis: any; yAxis: any; }[] = [];
    Object.entries(outlierValue).forEach((element: any) => {
      markpointValues.push({  name: 'Outlier', xAxis: element[0], yAxis: element[1] })
    });
    return markpointValues;
  }

  ngOnDestroy(): void {
    this.outlierDetectionServiceSubscription?.unsubscribe();
    this.options = undefined;
  }
  
  onNoClick(): void {
    this.dialogRef.close();
  }

  onChartInit(ec: any) {
    this.echartsIntance = ec;
  }

}


