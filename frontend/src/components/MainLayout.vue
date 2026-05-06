<template>
  <v-layout>
    <!-- Sidebar -->
    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      color="secondary"
      dark
    >
      <v-list-item class="pa-4" nav>
        <template v-slot:prepend>
          <img src="/caw-logo-dark.jpg" alt="CAW" class="sidebar-logo" />
        </template>
        <v-list-item-title class="text-white font-weight-bold">
          Ops Intelligence
        </v-list-item-title>
        <template v-slot:append>
          <v-btn
            icon="mdi-chevron-left"
            variant="text"
            color="white"
            size="small"
            @click="rail = !rail"
          />
        </template>
      </v-list-item>

      <v-divider color="rgba(255,255,255,0.2)" class="mb-2" />

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          :prepend-icon="item.icon"
          :title="item.title"
          color="primary"
          rounded="lg"
          class="mb-1"
        />
      </v-list>

      <template v-slot:append>
        <v-divider color="rgba(255,255,255,0.2)" class="mb-2" />
        <v-list density="compact" nav>
          <v-list-item
            prepend-icon="mdi-logout"
            title="Sair"
            color="primary"
            rounded="lg"
            @click="handleLogout"
          />
        </v-list>
        <div class="pa-3 text-center" v-if="!rail">
          <p class="text-caption text-white" style="opacity: 0.6;">
            {{ user?.full_name || 'Usuário' }}
          </p>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar flat color="white" elevation="1">
      <v-btn icon @click="rail = !rail" class="d-lg-none">
        <v-icon>mdi-menu</v-icon>
      </v-btn>

      <v-app-bar-title class="text-secondary">
        <span class="font-weight-bold">CAW</span>
        <span class="text-medium-emphasis ml-2">Ops Intelligence</span>
      </v-app-bar-title>

      <v-spacer />

      <v-chip color="primary" variant="tonal" class="mr-3">
        <v-icon start size="small">mdi-account-circle</v-icon>
        {{ user?.full_name || 'Usuário' }}
      </v-chip>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="bg-background">
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drawer = ref(true)
const rail = ref(false)

const user = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('caw_user') || '{}')
  } catch {
    return {}
  }
})

const menuItems = [
  { path: '/dashboard', icon: 'mdi-view-dashboard', title: 'Dashboard' },
  { path: '/projects', icon: 'mdi-folder-multiple', title: 'Projetos' },
  { path: '/projects/new', icon: 'mdi-plus-circle', title: 'Novo Projeto' },
  { path: '/risk-analysis', icon: 'mdi-alert-decagram', title: 'Análise de Risco' },
  { path: '/about', icon: 'mdi-information', title: 'Sobre o Sistema' },
]

function handleLogout() {
  localStorage.removeItem('caw_token')
  localStorage.removeItem('caw_user')
  router.push('/login')
}
</script>

<style scoped>
.sidebar-logo {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: cover;
}
</style>
