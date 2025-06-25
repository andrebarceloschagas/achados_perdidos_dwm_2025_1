import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CriarItemPage } from './criar-item.page';

describe('CriarItemPage', () => {
  let component: CriarItemPage;
  let fixture: ComponentFixture<CriarItemPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(CriarItemPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
