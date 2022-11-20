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



app.use(createPinia());
app.use(router);


app.mount('#app');