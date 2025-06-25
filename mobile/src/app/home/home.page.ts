import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { 
  AlertController,
  IonRefresher,
  IonRefresherContent,
  LoadingController, 
  ModalController,
  ToastController
} from '@ionic/angular/standalone';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent, 
  IonButtons, 
  IonButton,
  IonIcon,
  IonSegment,
  IonSegmentButton,
  IonLabel,
  IonSpinner,
  IonList,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonBadge,
  IonText,
  IonImg,
  IonFab,
  IonFabButton,
  RefresherCustomEvent
} from '@ionic/angular/standalone';

import { AuthService } from '../services/auth.service';
import { ItemService } from '../services/item.service';
import { User } from '../models/user.model';
import { Item } from '../models/item.model';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonHeader, 
    IonToolbar, 
    IonTitle, 
    IonContent,
    IonButtons,
    IonButton,
    IonIcon,
    IonSegment,
    IonSegmentButton,
    IonLabel,
    IonSpinner,
    IonList,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonBadge,
    IonText,
    IonImg,
    IonFab,
    IonFabButton,
    IonRefresher,
    IonRefresherContent
  ],
})
export class HomePage implements OnInit {
  user: User | null = null;
  itens: Item[] = [];
  loading: boolean = false;
  tipoFiltro: string = 'todos';
  
  constructor(
    private authService: AuthService,
    private itemService: ItemService,
    private router: Router,
    private alertController: AlertController,
    private toastController: ToastController,
    private loadingController: LoadingController,
    private modalController: ModalController
  ) {}

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      this.user = user;
    });
    this.carregarItens();
  }

  async carregarItens() {
    this.loading = true;
    
    let params: any = {
      page: 1,
      ordering: '-data_postagem' // Ordenar por data de postagem, mais recentes primeiro
    };
    
    // Adicionar filtro por tipo se não for "todos"
    if (this.tipoFiltro !== 'todos') {
      params.tipo = this.tipoFiltro;
    }
    
    try {
      const response = await firstValueFrom(this.itemService.getItens(params));
      this.itens = response?.results || [];
    } catch (error) {
      console.error('Erro ao carregar itens:', error);
      const toast = await this.toastController.create({
        message: 'Erro ao carregar itens. Tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
    } finally {
      this.loading = false;
    }
  }
  
  async handleRefresh(event: RefresherCustomEvent) {
    await this.carregarItens();
    event.target.complete();
  }

  filtrarPorTipo() {
    this.carregarItens();
  }
  
  /* Método buscarItens removido */
  
  verDetalhes(itemId: number) {
    this.router.navigate(['/item-detail', itemId]);
  }
  
  /* Função de reportar item removida */
  
  /* Método contatarDono removido */
  
  criarNovoItem() {
    this.router.navigate(['/criar-item']);
  }
  
  async logout() {
    const alert = await this.alertController.create({
      header: 'Sair',
      message: 'Deseja realmente sair do aplicativo?',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Sim',
          handler: () => {
            this.authService.logout().subscribe(() => {
              // O redirecionamento já é feito pelo AuthService
            });
          }
        }
      ]
    });
    
    await alert.present();
  }
}
