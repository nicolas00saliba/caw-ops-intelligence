<template>
  <div>
    <div class="d-flex align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-secondary">Projetos</h1>
        <p class="text-body-2 text-medium-emphasis">Gestão de projetos operacionais</p>
      </div>
      <v-spacer />
      <v-btn color="primary" to="/projects/new" prepend-icon="mdi-plus">
        Novo Projeto
      </v-btn>
    </div>

    <!-- Filtros -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="search"
              label="Buscar projeto..."
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="loadProjects"
            />
          </v-col>
          <v-col cols="6" md="2">
            <v-select
              v-model="filters.status"
              :items="filterOptions.statuses"
              label="Status"
              clearable
              hide-details
              @update:model-value="loadProjects"
            />
          </v-col>
          <v-col cols="6" md="2">
            <v-select
              v-model="filters.service_type"
              :items="filterOptions.service_types"
              label="Tipo de Serviço"
              clearable
              hide-details
              @update:model-value="loadProjects"
            />
          </v-col>
          <v-col cols="6" md="2">
            <v-select
              v-model="filters.priority"
              :items="filterOptions.priorities"
              label="Prioridade"
              clearable
              hide-details
              @update:model-value="loadProjects"
            />
          </v-col>
          <v-col cols="6" md="2">
            <v-select
              v-model="filters.risk_level"
              :items="filterOptions.risk_levels"
              label="Nível de Risco"
              clearable
              hide-details
              @update:model-value="loadProjects"
            />
          </v-col>
          <v-col cols="12" md="1" class="d-flex align-center">
            <v-btn icon variant="text" @click="clearFilters" title="Limpar filtros">
              <v-icon>mdi-filter-remove</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Tabela de Projetos -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="projects"
        :loading="loading"
        :items-per-page="15"
        class="projects-table"
        hover
      >
        <template v-slot:item.name="{ item }">
          <div class="py-2">
            <router-link :to="`/projects/${item.id}`" class="text-decoration-none font-weight-medium text-secondary">
              {{ item.name }}
            </router-link>
            <div class="text-caption text-medium-emphasis">{{ item.client }}</div>
          </div>
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small" variant="tonal">
            {{ item.status }}
          </v-chip>
        </template>

        <template v-slot:item.priority="{ item }">
          <v-chip :color="getPriorityColor(item.priority)" size="small" variant="flat">
            {{ item.priority }}
          </v-chip>
        </template>

        <template v-slot:item.risk_level="{ item }">
          <v-chip :color="getRiskColor(item.risk_level)" size="small" variant="tonal">
            <v-icon start size="x-small">mdi-alert-circle</v-icon>
            {{ item.risk_level }}
          </v-chip>
        </template>

        <template v-slot:item.current_stage="{ item }">
          <span class="text-body-2">{{ item.current_stage }}</span>
        </template>

        <template v-slot:item.estimated_cost="{ item }">
          <span class="text-body-2">{{ formatCurrency(item.estimated_cost) }}</span>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon size="small" variant="text" :to="`/projects/${item.id}`" title="Visualizar">
            <v-icon size="small">mdi-eye</v-icon>
          </v-btn>
          <v-btn icon size="small" variant="text" :to="`/projects/${item.id}/edit`" title="Editar">
            <v-icon size="small">mdi-pencil</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'

const projects = ref([])
const loading = ref(false)
const search = ref('')
const filters = ref({
  status: null,
  service_type: null,
  priority: null,
  risk_level: null,
})
const filterOptions = ref({
  statuses: [],
  service_types: [],
  cities: [],
  states: [],
  responsibles: [],
  priorities: [],
  risk_levels: [],
})

const headers = [
  { title: 'Projeto', key: 'name', sortable: true },
  { title: 'Tipo', key: 'service_type', sortable: true },
  { title: 'Etapa', key: 'current_stage', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Prioridade', key: 'priority', sortable: true },
  { title: 'Risco', key: 'risk_level', sortable: true },
  { title: 'Custo Estimado', key: 'estimated_cost', sortable: true },
  { title: 'Ações', key: 'actions', sortable: false, align: 'center' },
]

function getStatusColor(status) {
  const colors = {
    'Em andamento': 'info',
    'Finalizado': 'success',
    'Atrasado': 'error',
    'Pausado': 'warning',
  }
  return colors[status] || 'grey'
}

function getPriorityColor(priority) {
  const colors = {
    'Crítica': 'error',
    'Alta': 'warning',
    'Média': 'info',
    'Baixa': 'success',
  }
  return colors[priority] || 'grey'
}

function getRiskColor(level) {
  const colors = {
    'Alto': 'error',
    'Médio': 'warning',
    'Baixo': 'success',
  }
  return colors[level] || 'grey'
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
  }).format(value)
}

function clearFilters() {
  search.value = ''
  filters.value = { status: null, service_type: null, priority: null, risk_level: null }
  loadProjects()
}

async function loadProjects() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.service_type) params.service_type = filters.value.service_type
    if (filters.value.priority) params.priority = filters.value.priority
    if (filters.value.risk_level) params.risk_level = filters.value.risk_level

    const response = await api.get('/projects/', { params })
    projects.value = response.data
  } catch (error) {
    console.error('Erro ao carregar projetos:', error)
  } finally {
    loading.value = false
  }
}

async function loadFilterOptions() {
  try {
    const response = await api.get('/projects/filters')
    filterOptions.value = response.data
  } catch (error) {
    console.error('Erro ao carregar filtros:', error)
  }
}

onMounted(() => {
  loadFilterOptions()
  loadProjects()
})
</script>

<style scoped>
.projects-table :deep(th) {
  font-weight: 600 !important;
  text-transform: uppercase;
  font-size: 0.75rem !important;
  letter-spacing: 0.5px;
}
</style>
