import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { CriarItemComponent } from './criar-item.component';

describe('CriarItemComponent', () => {
  let component: CriarItemComponent;
  let fixture: ComponentFixture<CriarItemComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [CriarItemComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(CriarItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
