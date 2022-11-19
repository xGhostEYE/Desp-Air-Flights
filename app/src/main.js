import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'

// create the base app
const app = createApp(App);


// make the app use Pinia
app.use(createPinia());
// make the app use the vue router imported above
app.use(router);

// mount the app
app.mount('#app');