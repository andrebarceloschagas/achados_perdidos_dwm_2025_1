import { addIcons } from 'ionicons';
import { 
  // Navegação
  homeOutline, 
  searchOutline,
  menuOutline,
  arrowBackOutline,
  
  // Usuário
  personOutline,
  personCircleOutline,
  logInOutline, 
  logOutOutline,
  personAddOutline,
  
  // Ações de formulário
  eyeOutline,
  eyeOffOutline,
  saveOutline,
  addCircleOutline,
  createOutline,
  trashOutline,
  closeOutline,
  
  // Itens
  alertCircleOutline,
  checkmarkCircleOutline,
  informationCircleOutline,
  mailOutline,
  chatbubbleOutline,
  documentTextOutline,
  imageOutline,
  cameraOutline,
  locationOutline,
  calendarOutline,
  timeOutline
} from 'ionicons/icons';

export function registerIcons() {
  addIcons({
    // Navegação
    'home-outline': homeOutline,
    'search-outline': searchOutline,
    'menu-outline': menuOutline,
    'arrow-back-outline': arrowBackOutline,
    
    // Usuário
    'person-outline': personOutline,
    'person-circle-outline': personCircleOutline,
    'log-in-outline': logInOutline,
    'log-out-outline': logOutOutline,
    'person-add-outline': personAddOutline,
    
    // Ações de formulário
    'eye-outline': eyeOutline,
    'eye-off-outline': eyeOffOutline,
    'save-outline': saveOutline,
    'add-circle-outline': addCircleOutline,
    'create-outline': createOutline,
    'trash-outline': trashOutline,
    'close-outline': closeOutline,
    
    // Itens
    'alert-circle-outline': alertCircleOutline, // Para itens perdidos
    'checkmark-circle-outline': checkmarkCircleOutline, // Para itens encontrados
    'information-circle-outline': informationCircleOutline,
    'mail-outline': mailOutline,
    'chatbubble-outline': chatbubbleOutline,
    'document-text-outline': documentTextOutline,
    'image-outline': imageOutline,
    'camera-outline': cameraOutline,
    'location-outline': locationOutline,
    'calendar-outline': calendarOutline,
    'time-outline': timeOutline
  });
}
