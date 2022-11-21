import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import { BIconArrowDown, BIconExclamationCircle} from 'bootstrap-icons-vue';
const app = createApp(App);
app.component('BIconArrowDown', BIconArrowDown);
app.component('BIconExclamationCircle', BIconExclamationCircle);


// make the app use Pinia
app.use(createPinia());
// make the app use the vue router imported above
app.use(router);

// mount the app
app.mount('#app');