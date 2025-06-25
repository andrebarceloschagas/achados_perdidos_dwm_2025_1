import { Injectable, inject } from '@angular/core';
import {
  HttpRequest,
  HttpEvent,
  HttpInterceptorFn,
  HttpHandlerFn,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, BehaviorSubject, throwError, from } from 'rxjs';
import { catchError, filter, take, switchMap, finalize } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { RefreshTokenResponse } from '../models/auth.model';

// Novo interceptor funcional com melhor controle de refresh
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
  
  // Skip token for public endpoints
  if (req.url.includes('/token/') || 
      req.url.includes('/categorias/') || 
      req.url.includes('/blocos/') ||
      (req.url.includes('/users/') && req.method === 'POST')) {
    return next(req);
  }
  
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

// Gerenciamento de refresh token com melhor controle
let isRefreshing = false;
const refreshTokenSubject = new BehaviorSubject<string | null>(null);

const handle401Error = (
  request: HttpRequest<any>,
  next: HttpHandlerFn,
  authService: AuthService
): Observable<HttpEvent<any>> => {
  console.log('🚨 Erro 401 detectado, tentando refresh token...');
  
  if (!isRefreshing) {
    isRefreshing = true;
    refreshTokenSubject.next(null);
    
    return authService.refreshToken().pipe(
      switchMap((response: RefreshTokenResponse | null) => {
        if (response && response.access) {
          console.log('✅ Token renovado com sucesso, fazendo nova requisição');
          refreshTokenSubject.next(response.access);
          
          // Fazer nova requisição com token atualizado
          const newRequest = request.clone({
            setHeaders: {
              Authorization: `Bearer ${response.access}`
            }
          });
          
          return next(newRequest);
        }
        
        console.log('Falha ao renovar token, fazendo logout');
        // Se não conseguimos atualizar o token, precisamos fazer logout
        authService.logout().subscribe();
        return throwError(() => new Error('Sessão expirada. Por favor, faça login novamente.'));
      }),
      catchError(err => {
        console.log('Erro durante refresh token:', err);
        // Fazer logout ao falhar refresh
        authService.logout().subscribe();
        return throwError(() => err);
      }),
      finalize(() => {
        console.log('🏁 Finalizando processo de refresh');
        isRefreshing = false;
      })
    );
  }
  
  console.log('⏳ Aguardando refresh em andamento...');
  // Se já está fazendo refresh, aguardar o resultado
  return refreshTokenSubject.pipe(
    filter(token => token !== null),
    take(1),
    switchMap(token => {
      console.log('🔄 Usando token renovado para nova tentativa');
      const newRequest = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
      return next(newRequest);
    })
  );
};
