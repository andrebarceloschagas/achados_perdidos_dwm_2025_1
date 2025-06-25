import { Routes } from '@angular/router';
import { authGuard, loginGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then((m) => m.LoginPage),
    canActivate: [loginGuard]
  },
  {
    path: 'registro',
    loadComponent: () => import('./pages/registro/registro.page').then((m) => m.RegistroPage),
    canActivate: [loginGuard]
  },
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
    canActivate: [authGuard]
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'criar-item',
    loadComponent: () => import('./pages/criar-item/criar-item.page').then( m => m.CriarItemPage),
    canActivate: [authGuard]
  },
  {
    path: 'item-detail/:id',
    loadComponent: () => import('./pages/item-detail/item-detail.page').then( m => m.ItemDetailPage),
    canActivate: [authGuard]
  },
  {
    path: 'editar-item/:id',
    loadComponent: () => import('./pages/editar-item/editar-item.page').then( m => m.EditarItemPage),
    canActivate: [authGuard]
  },
];
