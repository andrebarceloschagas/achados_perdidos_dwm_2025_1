export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined?: string;
  itens_postados_count?: number;
  contatos_recebidos_count?: number;
}

export interface AuthResponse {
  refresh: string;
  access: string;
  user_id: number;
  username: string;
  name: string;
  is_staff: boolean;
}

export interface TokenData {
  id: number;
  jti: string;
  token: string;
  created_at: string;
  expires_at: string;
  blacklisted: boolean;
}

export interface TokensResponse {
  count: number;
  tokens: TokenData[];
}
