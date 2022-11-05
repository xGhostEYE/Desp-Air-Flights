import { createApp } from 'vue'
import { createPinia } from 'pinia'



import App from './App.vue'
import router from './router'

import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'

const app = createApp(App)

new Vue({
    el: "#app",
    components: { App },
    template: "<App/>"
  });  

app.use(createPinia())
app.use(router)

app.mount('#app')

