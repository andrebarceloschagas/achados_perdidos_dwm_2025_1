import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { AlertController, LoadingController } from '@ionic/angular/standalone';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent, 
  IonItem, 
  IonLabel, 
  IonInput, 
  IonButton, 
  IonSpinner,
  IonText,
  IonIcon,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonBackButton,
  IonButtons
} from '@ionic/angular/standalone';
// Os ícones agora são registrados globalmente em app.component.ts

@Component({
  selector: 'app-registro',
  templateUrl: './registro.page.html',
  styleUrls: ['./registro.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    IonHeader, 
    IonToolbar, 
    IonTitle, 
    IonContent, 
    IonItem, 
    IonLabel, 
    IonInput, 
    IonButton, 
    IonSpinner,
    IonText,
    IonIcon,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonBackButton,
    IonButtons
  ],
})
export class RegistroPage implements OnInit {
  registroForm: FormGroup;
  isSubmitting = false;
  hidePassword = true;
  hidePasswordConfirm = true;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private alertController: AlertController,
    private loadingController: LoadingController,
    private router: Router
  ) {
    this.registroForm = this.formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(4)]],
      email: ['', [Validators.required, Validators.email]],
      first_name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      password_confirm: ['', [Validators.required]]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  ngOnInit() {}

  // Validador personalizado para verificar se as senhas coincidem
  passwordMatchValidator(g: FormGroup) {
    const password = g.get('password')?.value;
    const passwordConfirm = g.get('password_confirm')?.value;

    return password === passwordConfirm ? null : { mismatch: true };
  }

  async onSubmit() {
    if (this.registroForm.invalid) {
      return;
    }

    this.isSubmitting = true;

    const loading = await this.loadingController.create({
      message: 'Criando conta...'
    });
    await loading.present();

    // Remover campo de confirmação de senha antes de enviar
    const userData = { ...this.registroForm.value };
    delete userData.password_confirm;

    this.authService.register(userData).subscribe({
      next: async () => {
        loading.dismiss();
        this.isSubmitting = false;
        
        const alert = await this.alertController.create({
          header: 'Conta criada',
          message: 'Sua conta foi criada com sucesso! Agora você pode fazer login.',
          buttons: [{
            text: 'OK',
            handler: () => {
              this.router.navigate(['/login']);
            }
          }]
        });
        
        await alert.present();
      },
      error: async (error) => {
        loading.dismiss();
        this.isSubmitting = false;
        
        let errorMessage = 'Ocorreu um erro ao criar a conta. Tente novamente.';
        
        if (error.error && typeof error.error === 'object') {
          const errorDetails = Object.entries(error.error)
            .map(([key, value]) => `${key}: ${value}`)
            .join('<br>');
          
          errorMessage = `Erro ao criar conta:<br>${errorDetails}`;
        }
        
        const alert = await this.alertController.create({
          header: 'Erro',
          message: errorMessage,
          buttons: ['OK']
        });
        
        await alert.present();
      }
    });
  }

  togglePasswordVisibility(field: 'password' | 'confirm') {
    if (field === 'password') {
      this.hidePassword = !this.hidePassword;
    } else {
      this.hidePasswordConfirm = !this.hidePasswordConfirm;
    }
  }
}
