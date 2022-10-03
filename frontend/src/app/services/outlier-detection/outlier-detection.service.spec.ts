import { TestBed } from '@angular/core/testing';

import { OutlierDetectionService } from './outlier-detection.service';

describe('OutlierDetectionService', () => {
  let service: OutlierDetectionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(OutlierDetectionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
