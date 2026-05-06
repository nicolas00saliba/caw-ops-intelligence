<template>
  <v-container fluid class="login-container fill-height">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="5" lg="4" xl="3">
        <v-card class="pa-8 login-card" elevation="12" rounded="xl">
          <v-card-text class="text-center">
            <img src="/caw-logo.png" alt="CAW Telecom e Energia" class="login-logo mb-4" />
            <h2 class="text-h5 font-weight-bold text-secondary mb-1">Ops Intelligence</h2>
            <p class="text-body-2 text-medium-emphasis mb-6">Gestão Operacional de Projetos</p>

            <v-form @submit.prevent="handleLogin" ref="form">
              <v-text-field
                v-model="username"
                label="Usuário"
                prepend-inner-icon="mdi-account"
                :error-messages="errors.username"
                class="mb-3"
                autofocus
              />
              <v-text-field
                v-model="password"
                label="Senha"
                prepend-inner-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                :error-messages="errors.password"
                class="mb-4"
              />

              <v-alert
                v-if="loginError"
                type="error"
                variant="tonal"
                class="mb-4"
                density="compact"
              >
                {{ loginError }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mb-4"
              >
                <v-icon start>mdi-login</v-icon>
                Acessar Sistema
              </v-btn>
            </v-form>

            <v-divider class="my-4" />
            <p class="text-caption text-medium-emphasis">
              <v-icon size="small" class="mr-1">mdi-shield-check</v-icon>
              Acesso restrito — Gestão Operacional CAW
            </p>
          </v-card-text>
        </v-card>

        <p class="text-center text-caption text-medium-emphasis mt-4">
          CAW Telecom e Energia &copy; {{ new Date().getFullYear() }} — Campo Largo/PR
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const loginError = ref('')
const errors = ref({ username: '', password: '' })

async function handleLogin() {
  errors.value = { username: '', password: '' }
  loginError.value = ''

  if (!username.value) {
    errors.value.username = 'Informe o usuário'
    return
  }
  if (!password.value) {
    errors.value.password = 'Informe a senha'
    return
  }

  loading.value = true
  try {
    const response = await api.post('/auth/login', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('caw_token', response.data.access_token)
    localStorage.setItem('caw_user', JSON.stringify(response.data.user))
    router.push('/dashboard')
  } catch (error) {
    loginError.value = error.response?.data?.detail || 'Erro ao realizar login'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #333333 0%, #1a1a1a 50%, #F5921B 100%);
  min-height: 100vh;
}

.login-card {
  backdrop-filter: blur(10px);
}

.login-logo {
  max-width: 200px;
  height: auto;
}
</style>
