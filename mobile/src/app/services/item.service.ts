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
      prioridade?: string,
      ordering?: string, // Para ordenação dos resultados (ex: '-data_postagem', 'titulo')
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
    
    // Garantir que os campos necessários são enviados corretamente
    Object.keys(item).forEach(key => {
      if (item[key] !== undefined && item[key] !== null) {
        // Se for um arquivo (foto)
        if (key === 'foto' && item[key] instanceof File) {
          try {
            formData.append(key, item[key], item[key].name);
          } catch (error) {
            console.error('Erro ao anexar foto:', error);
            // Continuar sem a foto se houver erro
          }
        } else if (key === 'data_ocorrencia' && typeof item[key] === 'string') {
          // Garantir que a data está no formato correto
          try {
            const data = new Date(item[key]);
            formData.append(key, data.toISOString().split('T')[0]); // Formato YYYY-MM-DD
          } catch (error) {
            formData.append(key, item[key]); // Usar o valor original se não conseguir formatar
          }
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

  // Obter todas as categorias de itens
  getCategorias(): Observable<{id: string, nome: string}[]> {
    return this.http.get<{id: string, nome: string}[]>(`${this.apiUrl}categorias/`);
  }

  // Obter todos os blocos/locais disponíveis
  getBlocos(): Observable<{id: string, nome: string}[]> {
    return this.http.get<{id: string, nome: string}[]>(`${this.apiUrl}blocos/`);
  }
  
  // Marcar um item como encontrado pelo dono
  marcarItemEncontrado(itemId: number): Observable<Item> {
    return this.http.post<Item>(`${this.apiUrl}itens/${itemId}/marcar_encontrado/`, {});
  }
  
  // Marcar um item como entregue
  marcarItemEntregue(itemId: number): Observable<Item> {
    return this.http.post<Item>(`${this.apiUrl}itens/${itemId}/marcar_entregue/`, {});
  }
  
  // Reportar um item como impróprio ou inadequado
  reportarItem(itemId: number, motivo: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}itens/${itemId}/reportar/`, { motivo });
  }
  
  // Obter comentários de um item específico
  getComentariosItem(itemId: number): Observable<Comentario[]> {
    return this.http.get<Comentario[]>(`${this.apiUrl}itens/${itemId}/comentarios/`);
  }
  
  // Excluir um comentário
  deleteComentario(comentarioId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}comentarios/${comentarioId}/`);
  }
  
  // Buscar itens similares a um item específico
  getItensSimilares(itemId: number): Observable<Item[]> {
    return this.http.get<Item[]>(`${this.apiUrl}itens/${itemId}/similares/`);
  }
  
  // Obter contatos enviados pelo usuário
  getContatosEnviados(): Observable<{count: number, results: ContatoItem[]}> {
    return this.http.get<{count: number, results: ContatoItem[]}>(`${this.apiUrl}contatos/enviados/`);
  }

  // Excluir um contato
  deleteContato(contatoId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}contatos/${contatoId}/`);
  }
  
  // Filtrar itens por proximidade (considerando o bloco/localização)
  getItensProximos(bloco: string): Observable<{count: number, results: Item[]}> {
    return this.getItens({ bloco });
  }
  
  // Obter apenas itens com prioridade alta
  getItensPrioritarios(): Observable<{count: number, results: Item[]}> {
    return this.getItens({ prioridade: 'true' });
  }
  
  // Buscar itens recentes
  getItensRecentes(): Observable<{count: number, results: Item[]}> {
    return this.getItens({ 
      page: 1,
      ordering: '-data_postagem' 
    });
  }
}
