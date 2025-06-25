import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditarItemPage } from './editar-item.page';

describe('EditarItemPage', () => {
  let component: EditarItemPage;
  let fixture: ComponentFixture<EditarItemPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(EditarItemPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
