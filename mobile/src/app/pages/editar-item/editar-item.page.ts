import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
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
import { ItemDetail } from '../../models/item.model';

@Component({
  selector: 'app-editar-item',
  templateUrl: './editar-item.page.html',
  styleUrls: ['./editar-item.page.scss'],
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
export class EditarItemPage implements OnInit {
  itemForm: FormGroup;
  categorias: {id: string, nome: string}[] = [];
  blocos: {id: string, nome: string}[] = [];
  imagemPreview: string | null = null;
  imagemArquivo: File | null = null;
  carregandoCategorias = false;
  carregandoBlocos = false;
  carregandoItem = false;
  enviando = false;
  dataHoje = new Date().toISOString();
  itemId: number | null = null;
  item: ItemDetail | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
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
    // Obter o ID do item da URL
    this.route.paramMap.subscribe(params => {
      const idParam = params.get('id');
      if (idParam) {
        this.itemId = parseInt(idParam, 10);
      }
    });

    if (this.itemId) {
      await Promise.all([
        this.carregarCategorias(),
        this.carregarBlocos(),
        this.carregarItem()
      ]);
    }
  }

  async carregarItem() {
    if (!this.itemId) return;
    
    this.carregandoItem = true;
    try {
      this.item = await firstValueFrom(this.itemService.getItem(this.itemId));
      
      // Preencher o formulário com os dados do item
      this.itemForm.patchValue({
        titulo: this.item.titulo,
        descricao: this.item.descricao,
        tipo: this.item.tipo,
        categoria: this.item.categoria,
        bloco: this.item.bloco,
        local_especifico: this.item.local_especifico || '',
        data_ocorrencia: this.item.data_ocorrencia,
        telefone_contato: this.item.telefone_contato || '',
        email_contato: this.item.email_contato || ''
      });

      // Se o item tem foto, mostrar preview
      if (this.item.foto) {
        this.imagemPreview = this.item.foto;
      }
    } catch (error) {
      console.error('Erro ao carregar item:', error);
      const toast = await this.toastController.create({
        message: 'Erro ao carregar dados do item. Tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
      this.router.navigate(['/home']);
    } finally {
      this.carregandoItem = false;
    }
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
    const cameraOptions = {
      quality: 90,
      allowEditing: true,
      resultType: CameraResultType.DataUrl,
      source: CameraSource.Prompt
    };
    
    const imageData = await Camera.getPhoto(cameraOptions);
    
    if (imageData && imageData.dataUrl) {
      this.imagemPreview = imageData.dataUrl;
      
      try {
        const response = await fetch(imageData.dataUrl);
        const blob = await response.blob();
        
        const fileName = new Date().getTime() + '.jpeg';
        this.imagemArquivo = new File([blob], fileName, { type: 'image/jpeg' });
        
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

  verificarTamanhoImagem(arquivo: File): boolean {
    const tamanhoMaximoMB = 5;
    const tamanhoMaximoBytes = tamanhoMaximoMB * 1024 * 1024;
    
    if (arquivo.size > tamanhoMaximoBytes) {
      this.toastController.create({
        message: `A imagem deve ter no máximo ${tamanhoMaximoMB}MB.`,
        duration: 3000,
        color: 'warning'
      }).then(toast => toast.present());
      return false;
    }
    return true;
  }

  removerImagem() {
    this.imagemPreview = null;
    this.imagemArquivo = null;
  }

  get formControls() {
    return this.itemForm.controls;
  }

  async atualizarItem() {
    if (!this.itemForm.valid || !this.itemId) {
      this.marcarCamposComoTocados();
      const toast = await this.toastController.create({
        message: 'Por favor, preencha todos os campos obrigatórios corretamente.',
        duration: 3000,
        color: 'warning'
      });
      await toast.present();
      return;
    }

    this.enviando = true;

    try {
      const loading = await this.loadingController.create({
        message: 'Atualizando item...',
        spinner: 'crescent'
      });
      await loading.present();

      const dadosItem = { ...this.itemForm.value };

      // Se uma nova imagem foi selecionada, incluí-la
      if (this.imagemArquivo) {
        dadosItem.foto = this.imagemArquivo;
      }

      await firstValueFrom(this.itemService.updateItem(this.itemId, dadosItem));

      loading.dismiss();

      const toast = await this.toastController.create({
        message: 'Item atualizado com sucesso!',
        duration: 3000,
        color: 'success'
      });
      await toast.present();

      // Voltar para a página de detalhes do item
      this.router.navigate(['/item-detail', this.itemId]);
    } catch (error) {
      console.error('Erro ao atualizar item:', error);
      
      const toast = await this.toastController.create({
        message: 'Erro ao atualizar o item. Verifique os dados e tente novamente.',
        duration: 3000,
        color: 'danger'
      });
      await toast.present();
    } finally {
      this.enviando = false;
    }
  }

  private marcarCamposComoTocados() {
    Object.keys(this.itemForm.controls).forEach(key => {
      this.itemForm.get(key)?.markAsTouched();
    });
  }

  cancelar() {
    if (this.itemId) {
      this.router.navigate(['/item-detail', this.itemId]);
    } else {
      this.router.navigate(['/home']);
    }
  }
}
