import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import {
  AlertController,
  LoadingController,
  ToastController
} from '@ionic/angular/standalone';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonBackButton,
  IonButton,
  IonIcon,
  IonLabel,
  IonSpinner,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonBadge,
  IonText,
  IonImg,
  IonCol,
  IonRow,
  IonGrid,
  IonChip
} from '@ionic/angular/standalone';

import { ItemService } from '../../services/item.service';
import { ItemDetail } from '../../models/item.model';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-item-detail',
  templateUrl: './item-detail.page.html',
  styleUrls: ['./item-detail.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonButtons,
    IonBackButton,
    IonButton,
    IonIcon,
    IonLabel,
    IonSpinner,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonBadge,
    IonText,
    IonImg,
    IonCol,
    IonRow,
    IonGrid,
    IonChip
  ]
})
export class ItemDetailPage implements OnInit {
  itemId: number | null = null;
  item: ItemDetail | null = null;
  loading = false;
  erroCarga = false;
  currentUserId: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private itemService: ItemService,
    private authService: AuthService,
    private loadingController: LoadingController,
    private toastController: ToastController,
    private alertController: AlertController
  ) {}

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.currentUserId = user.id;
      }
    });
    
    this.route.paramMap.subscribe(params => {
      const idParam = params.get('id');
      if (idParam) {
        this.itemId = parseInt(idParam, 10);
        this.carregarItem();
      } else {
        this.showError('Item não encontrado');
        this.router.navigate(['/home']);
      }
    });
  }

  async carregarItem() {
    if (!this.itemId) return;

    this.loading = true;
    this.erroCarga = false;
    
    try {
      const loading = await this.loadingController.create({
        message: 'Carregando detalhes...',
        spinner: 'crescent'
      });
      await loading.present();

      this.item = await firstValueFrom(this.itemService.getItem(this.itemId));
      loading.dismiss();
    } catch (error) {
      console.error('Erro ao carregar item:', error);
      this.erroCarga = true;
      this.showError('Não foi possível carregar os detalhes do item');
    } finally {
      this.loading = false;
    }
  }

  /* Método contatarDono removido */

  getNomeLocalOcorrencia(): string {
    if (!this.item) return '';
    
    let local = this.item.bloco_display || '';
    
    if (this.item.local_especifico) {
      local += this.item.local_especifico ? ` - ${this.item.local_especifico}` : '';
    }
    
    return local;
  }

  async showError(message: string) {
    const toast = await this.toastController.create({
      message,
      duration: 3000,
      color: 'danger'
    });
    toast.present();
  }

  voltar() {
    this.router.navigate(['/home']);
  }

  /* Método podeContatarDono removido */
  
  usuarioEhDono(): boolean {
    if (!this.item || !this.currentUserId) return false;
    return this.item.usuario === this.currentUserId;
  }
  
  editarItem() {
    if (!this.item) return;
    
    // Navegar para a página de edição passando o ID do item
    this.router.navigate(['/editar-item', this.item.id]);
  }
  
  async excluirItem() {
    if (!this.item) return;
    
    const alert = await this.alertController.create({
      header: 'Confirmar exclusão',
      message: `Tem certeza que deseja excluir o item "${this.item.titulo}"? Esta ação não pode ser desfeita.`,
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Excluir',
          role: 'destructive',
          handler: async () => {
            try {
              const loading = await this.loadingController.create({
                message: 'Excluindo item...',
                spinner: 'crescent'
              });
              await loading.present();
              
              await firstValueFrom(this.itemService.deleteItem(this.item!.id));
              
              loading.dismiss();
              
              const toast = await this.toastController.create({
                message: 'Item excluído com sucesso!',
                duration: 3000,
                color: 'success'
              });
              toast.present();
              
              // Voltar para a página inicial
              this.router.navigate(['/home']);
            } catch (error) {
              console.error('Erro ao excluir item:', error);
              this.showError('Não foi possível excluir o item. Tente novamente mais tarde.');
            }
          }
        }
      ]
    });
    
    await alert.present();
  }
}
