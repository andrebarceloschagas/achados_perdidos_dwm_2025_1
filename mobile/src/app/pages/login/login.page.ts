import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { AlertController, LoadingController } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
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
  IonCardContent
} from '@ionic/angular/standalone';
// Os ícones agora são registrados globalmente em app.component.ts

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
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
    IonCardContent
  ],
})
export class LoginPage implements OnInit {
  loginForm: FormGroup;
  isSubmitting = false;
  hidePassword = true;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private alertController: AlertController,
    private loadingController: LoadingController,
    private router: Router
  ) {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  ngOnInit() {}

  async onSubmit() {
    if (this.loginForm.invalid) {
      return;
    }

    this.isSubmitting = true;

    const loading = await this.loadingController.create({
      message: 'Autenticando...'
    });
    await loading.present();

    const { username, password } = this.loginForm.value;

    this.authService.login(username, password).subscribe({
      next: () => {
        loading.dismiss();
        this.isSubmitting = false;
      },
      error: async (error) => {
        loading.dismiss();
        this.isSubmitting = false;
        
        let errorMessage = 'Ocorreu um erro ao tentar fazer login. Tente novamente.';
        
        if (error.status === 401) {
          errorMessage = 'Usuário ou senha incorretos.';
        }
        
        const alert = await this.alertController.create({
          header: 'Erro de autenticação',
          message: errorMessage,
          buttons: ['OK']
        });
        
        await alert.present();
      }
    });
  }

  goToRegister() {
    this.router.navigate(['/registro']);
  }

  togglePasswordVisibility() {
    this.hidePassword = !this.hidePassword;
  }
}
