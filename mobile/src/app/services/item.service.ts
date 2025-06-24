import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Item, ItemDetail, Comentario, ContatoItem } from '../models/item.model';

@Injectable({
  providedIn: 'root'
})
export class ItemService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Obter lista de itens com filtros opcionais
  getItens(
    params?: { 
      page?: number, 
      tipo?: string, 
      categoria?: string, 
      bloco?: string,
      q?: string,
      status?: string,
      [key: string]: any // Adiciona index signature para permitir acesso dinâmico
    }
  ): Observable<{count: number, results: Item[]}> {
    let httpParams = new HttpParams();
    
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== undefined && params[key] !== null) {
          httpParams = httpParams.set(key, params[key].toString());
        }
      });
    }

    return this.http.get<{count: number, results: Item[]}>(`${this.apiUrl}itens/`, { params: httpParams });
  }

  // Obter detalhes de um item específico
  getItem(id: number): Observable<ItemDetail> {
    return this.http.get<ItemDetail>(`${this.apiUrl}itens/${id}/`);
  }

  // Obter itens postados pelo usuário logado
  getMeusItens(): Observable<{count: number, results: Item[]}> {
    return this.http.get<{count: number, results: Item[]}>(`${this.apiUrl}itens/meus_itens/`);
  }
  
  // Criar um novo item
  createItem(item: any): Observable<Item> {
    // Usar FormData para suportar upload de imagem
    const formData = new FormData();
    
    Object.keys(item).forEach(key => {
      if (item[key] !== undefined && item[key] !== null) {
        // Se for um arquivo (foto)
        if (key === 'foto' && item[key] instanceof File) {
          formData.append(key, item[key], item[key].name);
        } else {
          formData.append(key, item[key]);
        }
      }
    });
    
    return this.http.post<Item>(`${this.apiUrl}itens/`, formData);
  }

  // Atualizar um item existente
  updateItem(id: number, item: any): Observable<Item> {
    // Usar FormData para suportar upload de imagem
    const formData = new FormData();
    
    Object.keys(item).forEach(key => {
      if (item[key] !== undefined && item[key] !== null) {
        // Se for um arquivo (foto)
        if (key === 'foto' && item[key] instanceof File) {
          formData.append(key, item[key], item[key].name);
        } else {
          formData.append(key, item[key]);
        }
      }
    });
    
    return this.http.patch<Item>(`${this.apiUrl}itens/${id}/`, formData);
  }

  // Excluir um item
  deleteItem(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}itens/${id}/`);
  }

  // Adicionar um comentário a um item
  addComentario(itemId: number, texto: string): Observable<Comentario> {
    return this.http.post<Comentario>(`${this.apiUrl}comentarios/`, { item: itemId, texto });
  }

  // Enviar um contato para o dono do item
  createContato(itemId: number, mensagem: string): Observable<ContatoItem> {
    return this.http.post<ContatoItem>(`${this.apiUrl}contatos/`, { item: itemId, mensagem });
  }
  
  // Obter contatos recebidos pelo usuário
  getContatosRecebidos(): Observable<{count: number, results: ContatoItem[]}> {
    return this.http.get<{count: number, results: ContatoItem[]}>(`${this.apiUrl}contatos/recebidos/`);
  }

  // Marcar um contato como visualizado
  marcarContatoVisualizado(contatoId: number): Observable<ContatoItem> {
    return this.http.patch<ContatoItem>(`${this.apiUrl}contatos/${contatoId}/`, { visualizado: true });
  }
}
