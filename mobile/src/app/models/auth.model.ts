export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface AuthError {
  [key: string]: string[] | string;
}

export interface RefreshTokenResponse {
  access: string;
}
