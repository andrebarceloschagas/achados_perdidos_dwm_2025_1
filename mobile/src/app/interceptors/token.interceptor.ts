import { Injectable, inject } from '@angular/core';
import {
  HttpRequest,
  HttpEvent,
  HttpInterceptorFn,
  HttpHandlerFn,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, BehaviorSubject, throwError, from } from 'rxjs';
import { catchError, filter, take, switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { RefreshTokenResponse } from '../models/auth.model';

// Novo interceptor funcional
export const TokenInterceptor: HttpInterceptorFn = (
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> => {
  const authService = inject(AuthService);
  
  // Helper functions for token handling
  const addToken = (request: HttpRequest<any>, token: string): HttpRequest<any> => {
    return request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  };
  
  // Converter a promessa em um Observable
  return from(authService.getAccessToken()).pipe(
    switchMap(token => {
      if (token) {
        req = addToken(req, token);
      }
      
      return next(req).pipe(
        catchError((error: HttpErrorResponse) => {
          if (error instanceof HttpErrorResponse && error.status === 401) {
            return handle401Error(req, next, authService);
          }
          return throwError(() => error);
        })
      );
    })
  );
};

// Gerenciamento de refresh token
let isRefreshing = false;
const refreshTokenSubject = new BehaviorSubject<string | null>(null);

const handle401Error = (
  request: HttpRequest<any>,
  next: HttpHandlerFn,
  authService: AuthService
): Observable<HttpEvent<any>> => {
  if (!isRefreshing) {
    isRefreshing = true;
    refreshTokenSubject.next(null);
    
    return authService.refreshToken().pipe(
      switchMap((response: RefreshTokenResponse | null) => {
        isRefreshing = false;
        
        if (response && response.access) {
          refreshTokenSubject.next(response.access);
          return next(request.clone({
            setHeaders: {
              Authorization: `Bearer ${response.access}`
            }
          }));
        }
        
        // Se não conseguimos atualizar o token, precisamos fazer logout
        authService.logout().subscribe();
        return throwError(() => new Error('Sessão expirada. Por favor, faça login novamente.'));
      }),
      catchError(err => {
        isRefreshing = false;
        
        // Fazer logout ao falhar refresh
        authService.logout().subscribe();
        return throwError(() => err);
      })
    );
  }
  
  return refreshTokenSubject.pipe(
    filter(token => token !== null),
    take(1),
    switchMap(token => next(request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    })))
  );
};
