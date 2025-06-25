export interface Item {
  id: number;
  titulo: string;
  descricao: string;
  categoria: string;
  categoria_display: string;
  tipo: 'perdido' | 'encontrado';
  tipo_display: string;
  bloco: string;
  bloco_display: string;
  local_especifico?: string;
  foto?: string;
  data_postagem: string;
  data_ocorrencia: string;
  data_atualizacao: string;
  usuario: number;
  usuario_nome: string;
  status: string;
  status_display: string;
  telefone_contato?: string;
  email_contato?: string;
  visualizacoes: number;
  prioridade: boolean;
  tempo_desde_postagem: string;
}

export interface ItemDetail extends Item {
  contatos_count: number;
}

// Interface Comentario removida

// Interface ContatoItem removida
