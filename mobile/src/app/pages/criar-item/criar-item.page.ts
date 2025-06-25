import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Camera, CameraResultType, CameraSource, Photo } from '@capacitor/camera';
import { Capacitor } from '@capacitor/core';
import { firstValueFrom } from 'rxjs';
import { 
  AlertController, 
  LoadingController, 
  ToastController 
} from '@ionic/angular/standalone';
import { 
  IonContent, 
  IonHeader, 
  IonTitle, 
  IonToolbar,
  IonButtons,
  IonBackButton,
  IonLabel,
  IonInput,
  IonTextarea,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonItem,
  IonDatetime,
  IonDatetimeButton,
  IonModal,
  IonIcon,
  IonSegment,
  IonSegmentButton,
  IonImg,
  IonSpinner,
  IonText
} from '@ionic/angular/standalone';

import { ItemService } from '../../services/item.service';

@Component({
  selector: 'app-criar-item',
  templateUrl: './criar-item.page.html',
  styleUrls: ['./criar-item.page.scss'],
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule,
    ReactiveFormsModule,
    IonContent, 
    IonHeader, 
    IonTitle, 
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonLabel,
    IonInput,
    IonTextarea,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonItem,
    IonDatetime,
    IonDatetimeButton,
    IonModal,
    IonIcon,
    IonSegment,
    IonSegmentButton,
    IonImg,
    IonSpinner,
    IonText
  ]
})
export class CriarItemPage implements OnInit {
  itemForm: FormGroup;
  categorias: {id: string, nome: string}[] = [];
  blocos: {id: string, nome: string}[] = [];
  imagemPreview: string | null = null;
  imagemArquivo: File | null = null;
  carregandoCategorias = false;
  carregandoBlocos = false;
  enviando = false;
  dataHoje = new Date().toISOString();

  constructor(
    private formBuilder: FormBuilder,
    private itemService: ItemService,
    private router: Router,
    private loadingController: LoadingController,
    private toastController: ToastController,
    private alertController: AlertController
  ) { 
    this.itemForm = this.formBuilder.group({
      titulo: ['', [Validators.required, Validators.minLength(5), Validators.maxLength(100)]],
      descricao: ['', [Validators.required, Validators.minLength(10)]],
      tipo: ['perdido', Validators.required],
      categoria: ['', Validators.required],
      bloco: ['', Validators.required],
      local_especifico: [''],
      data_ocorrencia: [this.dataHoje, Validators.required],
      telefone_contato: [''],
      email_contato: ['', Validators.email]
    });
  }

  async ngOnInit() {
    await Promise.all([
      this.carregarCategorias(),
      this.carregarBlocos()
    ]);
  }

  async carregarCategorias() {
    this.carregandoCategorias = true;
    try {
      this.categorias = await firstValueFrom(this.itemService.getCategorias());
    } catch (error) {
      console.error('Erro ao carregar categorias:', error);
      const toast = await this.toastController.create({
        message: 'Erro ao carregar categorias. Por favor, tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
    } finally {
      this.carregandoCategorias = false;
    }
  }

  async carregarBlocos() {
    this.carregandoBlocos = true;
    try {
      this.blocos = await firstValueFrom(this.itemService.getBlocos());
    } catch (error) {
      console.error('Erro ao carregar blocos:', error);
      const toast = await this.toastController.create({
        message: 'Erro ao carregar blocos/locais. Por favor, tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
    } finally {
      this.carregandoBlocos = false;
    }
  }

  async selecionarImagem() {
    try {
      // Verificar se estamos em um ambiente que suporta a API de câmera do Capacitor
      const isNative = Capacitor.isPluginAvailable('Camera');
      let imageData: Photo;
      
      if (isNative) {
        // Usar o plugin Camera em ambientes nativos
        imageData = await Camera.getPhoto({
          quality: 90,
          allowEditing: true,
          resultType: CameraResultType.DataUrl,
          source: CameraSource.Prompt
        });
      } else {
        // Fallback para navegadores web: usar método alternativo
        // Mostrar alerta para o usuário sobre limitações no navegador
        await this.alertController.create({
          header: 'Atenção',
          message: 'Para a melhor experiência no upload de imagens, use o aplicativo móvel instalado.',
          buttons: ['OK']
        }).then(alert => alert.present());
        
        // Mesmo fluxo, mas com possíveis limitações
        imageData = await Camera.getPhoto({
          quality: 90,
          allowEditing: true,
          resultType: CameraResultType.DataUrl,
          source: CameraSource.Prompt
        });
      }
      
      if (imageData && imageData.dataUrl) {
        this.imagemPreview = imageData.dataUrl;
        
        try {
          // Converter a imagem de base64 para File
          const response = await fetch(imageData.dataUrl);
          const blob = await response.blob();
          
          // Usar timestamp para garantir nome único
          const fileName = new Date().getTime() + '.jpeg';
          this.imagemArquivo = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
        } catch (conversionError) {
          console.error('Erro ao converter imagem:', conversionError);
          
          // Fallback: tentar criar um blob diretamente do base64
          try {
            const base64Data = imageData.dataUrl.split(',')[1];
            const byteCharacters = atob(base64Data);
            const byteArrays = [];
            
            for (let i = 0; i < byteCharacters.length; i++) {
              byteArrays.push(byteCharacters.charCodeAt(i));
            }
            
            const byteArray = new Uint8Array(byteArrays);
            const blob = new Blob([byteArray], {type: 'image/jpeg'});
            
            const fileName = new Date().getTime() + '.jpeg';
            this.imagemArquivo = new File([blob], fileName, { type: 'image/jpeg' });
          } catch (fallbackError) {
            console.error('Fallback para conversão de imagem falhou:', fallbackError);
            throw new Error('Não foi possível processar a imagem');
          }
        }
      }
    } catch (error) {
      console.error('Erro ao selecionar imagem:', error);
      const toast = await this.toastController.create({
        message: 'Erro ao selecionar imagem. Por favor, tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
    }
  }

  removerImagem() {
    this.imagemPreview = null;
    this.imagemArquivo = null;
  }

  // Função auxiliar para tratar erros de upload e limites de tamanho
  verificarTamanhoImagem(file: File): boolean {
    // Limite de 5MB para fotos
    const limiteTamanho = 5 * 1024 * 1024; // 5MB em bytes
    
    if (file.size > limiteTamanho) {
      this.toastController.create({
        message: 'A imagem é muito grande. O tamanho máximo permitido é 5MB.',
        duration: 3000,
        color: 'danger'
      }).then(toast => toast.present());
      
      return false;
    }
    
    return true;
  }

  async enviarItem() {
    if (this.itemForm.invalid) {
      this.marcarCamposInvalidos();
      return;
    }

    this.enviando = true;
    
    const loading = await this.loadingController.create({
      message: 'Salvando item...',
      spinner: 'crescent'
    });
    await loading.present();
    
    try {
      // Clone o valor do formulário para não alterar o original
      const itemData = {...this.itemForm.value};
      
      // Formatar a data corretamente (pode ser necessário dependendo da API)
      if (itemData.data_ocorrencia) {
        try {
          const data = new Date(itemData.data_ocorrencia);
          if (!isNaN(data.getTime())) {
            itemData.data_ocorrencia = data.toISOString().split('T')[0]; // Formato YYYY-MM-DD
          }
        } catch (error) {
          console.error('Erro ao formatar data:', error);
          // Manter o valor original se houver erro
        }
      }
      
      // Adicionar foto se existe e se passar na validação de tamanho
      if (this.imagemArquivo) {
        if (this.verificarTamanhoImagem(this.imagemArquivo)) {
          itemData.foto = this.imagemArquivo;
        } else {
          // Se a imagem for muito grande, perguntar se quer continuar sem a imagem
          const continuar = await this.alertController.create({
            header: 'Imagem muito grande',
            message: 'A imagem selecionada excede o tamanho limite. Deseja continuar sem a imagem?',
            buttons: [
              {
                text: 'Cancelar',
                role: 'cancel',
                handler: () => {
                  loading.dismiss();
                  this.enviando = false;
                  return false;
                }
              },
              {
                text: 'Continuar',
                handler: () => true
              }
            ]
          });
          
          await continuar.present();
          const { role } = await continuar.onDidDismiss();
          
          if (role === 'cancel') {
            return; // Interrompe o envio
          }
          // Continua sem a imagem
        }
      }
      
      // Enviar para a API
      await firstValueFrom(this.itemService.createItem(itemData));
      
      // Mostrar mensagem de sucesso
      const toast = await this.toastController.create({
        message: 'Item cadastrado com sucesso!',
        duration: 3000,
        color: 'success'
      });
      await toast.present();
      
      // Voltar para a home
      this.router.navigate(['/home']);
    } catch (error) {
      console.error('Erro ao cadastrar item:', error);
      
      const toast = await this.toastController.create({
        message: 'Erro ao cadastrar item. Por favor, tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
    } finally {
      loading.dismiss();
      this.enviando = false;
    }
  }

  marcarCamposInvalidos() {
    Object.keys(this.itemForm.controls).forEach(campo => {
      const control = this.itemForm.get(campo);
      if (control?.invalid) {
        control.markAsTouched();
      }
    });
    
    // Exibir alerta sobre campos obrigatórios
    this.alertController.create({
      header: 'Formulário incompleto',
      message: 'Por favor, preencha todos os campos obrigatórios corretamente.',
      buttons: ['OK']
    }).then(alert => alert.present());
  }

  get formControls(): any {
    return this.itemForm.controls;
  }

  cancelar() {
    this.router.navigate(['/home']);
  }

  // Método alternativo para criar arquivo de texto se o upload de imagem falhar
  criarArquivoTexto(descricaoImagem: string): File {
    const conteudo = `Descrição da imagem: ${descricaoImagem || 'Não fornecida'}\nData: ${new Date().toLocaleString()}`;
    return new File([conteudo], 'descricao-imagem.txt', { type: 'text/plain' });
  }
}
