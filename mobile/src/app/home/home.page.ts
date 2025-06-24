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
  IonSearchbar,
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
    IonSearchbar,
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
  searchText: string = '';
  
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
      page: 1
    };
    
    // Adicionar filtro por tipo se não for "todos"
    if (this.tipoFiltro !== 'todos') {
      params.tipo = this.tipoFiltro;
    }
    
    // Adicionar texto de busca se existir
    if (this.searchText && this.searchText.trim() !== '') {
      params.q = this.searchText.trim();
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
  
  buscarItens() {
    this.carregarItens();
  }
  
  verDetalhes(itemId: number) {
    // Navegar para a página de detalhes (ainda será implementada)
    // this.router.navigate(['/item-detalhes', itemId]);
    this.alertController.create({
      header: 'Detalhes do Item',
      message: 'Página de detalhes em implementação',
      buttons: ['OK']
    }).then(alert => alert.present());
  }
  
  async contatarDono(item: Item) {
    const alert = await this.alertController.create({
      header: 'Contatar dono',
      message: `Deseja enviar uma mensagem para o dono de "${item.titulo}"?`,
      inputs: [
        {
          name: 'mensagem',
          type: 'textarea',
          placeholder: 'Digite sua mensagem...'
        }
      ],
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Enviar',
          handler: async (data) => {
            if (data.mensagem && data.mensagem.trim() !== '') {
              try {
                const loading = await this.loadingController.create({
                  message: 'Enviando mensagem...'
                });
                await loading.present();
                
                await firstValueFrom(this.itemService.createContato(item.id, data.mensagem));
                
                await loading.dismiss();
                const toast = await this.toastController.create({
                  message: 'Mensagem enviada com sucesso!',
                  duration: 3000,
                  color: 'success'
                });
                await toast.present();
              } catch (error) {
                console.error('Erro ao enviar mensagem:', error);
                const toast = await this.toastController.create({
                  message: 'Erro ao enviar mensagem. Tente novamente.',
                  duration: 3000,
                  color: 'danger'
                });
                await toast.present();
              }
            }
          }
        }
      ]
    });
    
    await alert.present();
  }
  
  criarNovoItem() {
    // Navegar para a página de criação de item (ainda será implementada)
    // this.router.navigate(['/criar-item']);
    this.alertController.create({
      header: 'Novo Item',
      message: 'Página de criação de itens em implementação',
      buttons: ['OK']
    }).then(alert => alert.present());
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
