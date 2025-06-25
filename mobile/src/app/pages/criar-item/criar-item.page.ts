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
      // Verificar se estamos em ambiente web para mostrar opções diferentes
      if (Capacitor.getPlatform() === 'web') {
        await this.selecionarImagemWeb();
      } else {
        await this.selecionarImagemMobile();
      }
    } catch (error) {
      console.error('Erro ao selecionar imagem:', error);
      await this.toastController.create({
        message: 'Erro ao selecionar imagem. Por favor, tente novamente.',
        duration: 3000,
        color: 'danger'
      }).then(toast => toast.present());
    }
  }

  async selecionarImagemWeb() {
    // Criar input file para selecionar do computador
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    
    input.onchange = async (event: any) => {
      const file = event.target.files[0];
      if (file) {
        // Verificar tamanho do arquivo
        if (!this.verificarTamanhoImagem(file)) {
          return;
        }

        // Criar preview da imagem
        const reader = new FileReader();
        reader.onload = async (e: any) => {
          this.imagemPreview = e.target.result;
          
          // Copiar arquivo para a pasta de assets
          await this.salvarImagemLocal(file);
        };
        reader.readAsDataURL(file);
      }
    };
    
    input.click();
  }

  async selecionarImagemMobile() {
    // Configuração da câmera para ambos os ambientes
    const cameraOptions = {
      quality: 90,
      allowEditing: true,
      resultType: CameraResultType.DataUrl,
      source: CameraSource.Prompt
    };
    
    // Obter imagem da câmera ou galeria
    const imageData = await Camera.getPhoto(cameraOptions);
    
    if (imageData && imageData.dataUrl) {
      this.imagemPreview = imageData.dataUrl;
      
      try {
        // Método mais confiável de converter base64 para File
        const response = await fetch(imageData.dataUrl);
        const blob = await response.blob();
        
        // Usar timestamp para garantir nome único
        const fileName = new Date().getTime() + '.jpeg';
        this.imagemArquivo = new File([blob], fileName, { type: 'image/jpeg' });
        
        // Verificar tamanho do arquivo imediatamente
        if (!this.verificarTamanhoImagem(this.imagemArquivo)) {
          this.imagemPreview = null;
          this.imagemArquivo = null;
        }
      } catch (error) {
        console.error('Erro ao processar imagem:', error);
        await this.toastController.create({
          message: 'Erro ao processar a imagem. Por favor, tente novamente.',
          duration: 3000,
          color: 'danger'
        }).then(toast => toast.present());
        
        this.imagemPreview = null;
        this.imagemArquivo = null;
      }
    }
  }

  async salvarImagemLocal(file: File) {
    try {
      // Gerar nome único para o arquivo
      const timestamp = new Date().getTime();
      const extension = file.name.split('.').pop() || 'jpg';
      const fileName = `item_${timestamp}.${extension}`;
      
      // Para desenvolvimento web, vamos usar o arquivo diretamente
      // Em produção, seria necessário implementar upload para servidor
      this.imagemArquivo = new File([file], fileName, { type: file.type });
      
      // Salvar referência para uso posterior
      localStorage.setItem('ultimaImagemSelecionada', fileName);
      
      console.log('Imagem preparada para upload:', fileName);
    } catch (error) {
      console.error('Erro ao processar imagem local:', error);
      throw error;
    }
  }

  removerImagem() {
    this.imagemPreview = null;
    this.imagemArquivo = null;
  }

  /**
   * Verifica se o tamanho da imagem está dentro do limite máximo permitido
   * @param file Arquivo para verificar o tamanho
   * @returns true se o arquivo está dentro do limite, false caso contrário
   */
  verificarTamanhoImagem(file: File): boolean {
    if (!file) return false;
    
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
    
    // Verificar tipos de arquivo permitidos
    const tiposPermitidos = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!tiposPermitidos.includes(file.type)) {
      this.toastController.create({
        message: 'Formato de imagem não suportado. Por favor, use JPEG ou PNG.',
        duration: 3000,
        color: 'danger'
      }).then(toast => toast.present());
      
      return false;
    }
    
    return true;
  }

  async enviarItem() {
    // Validação inicial do formulário
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
      
      // Formatar a data corretamente para o formato esperado pela API
      if (itemData.data_ocorrencia) {
        const data = new Date(itemData.data_ocorrencia);
        if (!isNaN(data.getTime())) {
          itemData.data_ocorrencia = data.toISOString().split('T')[0]; // Formato YYYY-MM-DD
        }
      }
      
      // Limpar campos vazios para evitar problemas no backend
      Object.keys(itemData).forEach(key => {
        if (itemData[key] === '' || itemData[key] === null || itemData[key] === undefined) {
          delete itemData[key];
        }
      });
      
      // Adicionar foto se existir e estiver dentro do limite de tamanho
      if (this.imagemArquivo) {
        if (this.verificarTamanhoImagem(this.imagemArquivo)) {
          itemData.foto = this.imagemArquivo;
        } else {
          const continuar = await this.alertController.create({
            header: 'Imagem muito grande',
            message: 'A imagem selecionada excede o tamanho limite de 5MB. Deseja continuar sem a imagem?',
            buttons: [
              {
                text: 'Cancelar',
                role: 'cancel'
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
            loading.dismiss();
            this.enviando = false;
            return; // Interrompe o envio
          }
          // Continua sem a imagem
        }
      }
      
      // Enviar para a API
      const response = await firstValueFrom(this.itemService.createItem(itemData));
      
      // Mostrar mensagem de sucesso
      const toast = await this.toastController.create({
        message: 'Item cadastrado com sucesso!',
        duration: 3000,
        color: 'success'
      });
      await toast.present();
      
      // Voltar para a home
      this.router.navigate(['/home']);
    } catch (error: any) {
      console.error('Erro ao cadastrar item:', error);
      
      // Tratamento mais detalhado do erro
      let mensagemErro = 'Erro ao cadastrar item. Por favor, tente novamente.';
      
      if (error.status === 400 && error.error) {
        // Tentar extrair mensagens específicas de erro do backend
        const erros = Object.entries(error.error)
          .map(([campo, msgs]) => `${campo}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
          .join('; ');
        
        if (erros) {
          mensagemErro = `Erro nos dados: ${erros}`;
        }
      } else if (error.status === 0 || error.status === 503) {
        mensagemErro = 'Erro de conexão com o servidor. Verifique sua internet e tente novamente.';
      }
      
      const toast = await this.toastController.create({
        message: mensagemErro,
        duration: 5000,
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
}
