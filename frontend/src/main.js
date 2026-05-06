import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import VueApexCharts from 'vue3-apexcharts'

import App from './App.vue'
import router from './router/index.js'

const cawTheme = {
  dark: false,
  colors: {
    primary: '#F5921B',
    secondary: '#333333',
    accent: '#1B5E20',
    error: '#D32F2F',
    warning: '#F57C00',
    info: '#1976D2',
    success: '#388E3C',
    background: '#F5F5F5',
    surface: '#FFFFFF',
    'on-primary': '#FFFFFF',
    'on-secondary': '#FFFFFF',
  },
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'cawTheme',
    themes: {
      cawTheme,
    },
  },
  defaults: {
    VBtn: {
      rounded: 'lg',
    },
    VCard: {
      rounded: 'lg',
      elevation: 2,
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
    },
  },
})

const app = createApp(App)
app.use(vuetify)
app.use(router)
app.use(VueApexCharts)
app.mount('#app')
