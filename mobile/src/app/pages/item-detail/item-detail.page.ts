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
  IonList,
  IonItem,
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
    IonList,
    IonItem,
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
  comentarioTexto = '';
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
    // Get the current user
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

  async contatarDono() {
    if (!this.item) return;

    const alert = await this.alertController.create({
      header: 'Contatar dono',
      message: `Deseja enviar uma mensagem para o dono de "${this.item.titulo}"?`,
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
            if (data.mensagem?.trim()) {
              try {
                const loading = await this.loadingController.create({
                  message: 'Enviando mensagem...'
                });
                await loading.present();
                
                await firstValueFrom(this.itemService.createContato(this.item!.id, data.mensagem));
                
                loading.dismiss();
                const toast = await this.toastController.create({
                  message: 'Mensagem enviada com sucesso!',
                  duration: 3000,
                  color: 'success'
                });
                toast.present();
              } catch (error) {
                console.error('Erro ao enviar mensagem:', error);
                this.showError('Erro ao enviar mensagem. Tente novamente.');
              }
            }
          }
        }
      ]
    });
    
    await alert.present();
  }

  async adicionarComentario() {
    if (!this.item || !this.comentarioTexto.trim()) return;

    try {
      const loading = await this.loadingController.create({
        message: 'Enviando comentário...',
        spinner: 'crescent'
      });
      await loading.present();

      await firstValueFrom(this.itemService.addComentario(this.item.id, this.comentarioTexto));
      
      // Limpar o campo de comentário
      this.comentarioTexto = '';
      
      // Recarregar item para atualizar comentários
      await this.carregarItem();
      
      loading.dismiss();
      const toast = await this.toastController.create({
        message: 'Comentário adicionado com sucesso!',
        duration: 2000,
        color: 'success'
      });
      toast.present();
    } catch (error) {
      console.error('Erro ao adicionar comentário:', error);
      this.showError('Erro ao adicionar comentário. Tente novamente.');
    }
  }

  async reportarItem() {
    if (!this.item) return;

    const alert = await this.alertController.create({
      header: 'Reportar Item',
      message: `Deseja reportar "${this.item.titulo}" como impróprio ou inadequado?`,
      inputs: [
        {
          name: 'motivo',
          type: 'textarea',
          placeholder: 'Informe o motivo da denúncia'
        }
      ],
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Reportar',
          handler: async (data) => {
            if (data.motivo?.trim()) {
              try {
                const loading = await this.loadingController.create({
                  message: 'Enviando denúncia...'
                });
                await loading.present();
                
                await firstValueFrom(this.itemService.reportarItem(this.item!.id, data.motivo));
                
                loading.dismiss();
                const toast = await this.toastController.create({
                  message: 'Item reportado com sucesso!',
                  duration: 3000,
                  color: 'success'
                });
                toast.present();
              } catch (error) {
                console.error('Erro ao reportar item:', error);
                this.showError('Erro ao reportar item. Tente novamente.');
              }
            }
          }
        }
      ]
    });
    
    await alert.present();
  }

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

  podeContatarDono(): boolean {
    if (!this.item) return false;
    return this.item.tipo === 'encontrado';
  }
  
  usuarioEhDono(): boolean {
    if (!this.item || !this.currentUserId) return false;
    return this.item.usuario === this.currentUserId;
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
