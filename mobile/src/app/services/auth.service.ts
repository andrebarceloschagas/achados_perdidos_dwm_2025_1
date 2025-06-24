import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, from, of } from 'rxjs';
import { map, switchMap, tap } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import { AuthResponse, User, TokensResponse } from '../models/user.model';
import { RefreshTokenResponse } from '../models/auth.model';
import { Storage } from '@ionic/storage-angular';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  private tokenExpirationTimer: any;

  constructor(
    private http: HttpClient,
    private storage: Storage,
    private router: Router
  ) {
    this.initStorage();
  }

  async initStorage() {
    await this.storage.create();
    this.checkToken();
  }

  // Verifica se o token está armazenado ao iniciar o app
  async checkToken() {
    const tokens = await this.getStoredTokens();
    if (tokens && tokens.access) {
      this.getUserInfo().subscribe({
        next: (user) => this.currentUserSubject.next(user),
        error: () => this.logout()
      });
    }
  }

  // Login com usuário e senha
  login(username: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}token/`, { username, password })
      .pipe(
        tap(response => this.setAuthData(response)),
      );
  }

  // Registrar novo usuário
  register(userData: any): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}users/`, userData);
  }

  // Buscar informações do usuário logado
  getUserInfo(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}users/me/`);
  }

  // Obter tokens ativos do usuário
  getUserTokens(): Observable<TokensResponse> {
    return this.http.get<TokensResponse>(`${this.apiUrl}users/tokens/`);
  }

  // Revogar um token específico
  revokeToken(tokenId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}token/revoke/${tokenId}/`, {});
  }

  // Revogar todos os tokens exceto o atual
  revokeAllTokens(): Observable<any> {
    return this.http.post(`${this.apiUrl}token/revoke-all/`, {});
  }

  // Fazer logout
  logout(): Observable<any> {
    // Obter refresh token do storage
    return from(this.getStoredTokens()).pipe(
      switchMap(tokens => {
        if (tokens && tokens.refresh) {
          // Enviar requisição para blacklist
          return this.http.post(`${this.apiUrl}logout/`, { refresh: tokens.refresh }).pipe(
            tap(() => this.clearAuthData())
          );
        } else {
          // Apenas limpar dados locais se não tiver token
          this.clearAuthData();
          return of(null);
        }
      })
    );
  }

  // Refresh token
  refreshToken(): Observable<RefreshTokenResponse | null> {
    return from(this.getStoredTokens()).pipe(
      switchMap(tokens => {
        if (!tokens || !tokens.refresh) {
          return of(null);
        }
        return this.http.post<RefreshTokenResponse>(`${this.apiUrl}token/refresh/`, {
          refresh: tokens.refresh
        }).pipe(
          tap(response => this.updateAccessToken(response.access))
        );
      })
    );
  }

  // Verificar se o usuário está autenticado
  isAuthenticated(): Promise<boolean> {
    return this.storage.get('tokens').then(tokens => {
      return !!tokens && !!tokens.access;
    });
  }

  // Obter tokens armazenados
  async getStoredTokens(): Promise<{access: string, refresh: string} | null> {
    return await this.storage.get('tokens');
  }

  // Obter o access token
  async getAccessToken(): Promise<string | null> {
    const tokens = await this.getStoredTokens();
    return tokens ? tokens.access : null;
  }

  // Configurar dados de autenticação
  private async setAuthData(response: AuthResponse) {
    // Armazenar tokens
    await this.storage.set('tokens', {
      access: response.access,
      refresh: response.refresh
    });

    // Buscar informações completas do usuário
    this.getUserInfo().subscribe(user => {
      this.currentUserSubject.next(user);
      this.router.navigate(['/home']);
    });
  }

  // Atualizar apenas o access token
  private async updateAccessToken(access: string) {
    const tokens = await this.getStoredTokens();
    if (tokens) {
      tokens.access = access;
      await this.storage.set('tokens', tokens);
    }
  }

  // Limpar dados de autenticação
  private clearAuthData() {
    this.storage.remove('tokens');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
    if (this.tokenExpirationTimer) {
      clearTimeout(this.tokenExpirationTimer);
    }
  }

  // Obter usuário atual
  get currentUser(): User | null {
    return this.currentUserSubject.value;
  }
}
