<template>
  <div v-if="project">
    <!-- Header -->
    <div class="d-flex align-center mb-6">
      <v-btn icon variant="text" to="/projects" class="mr-3">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <div>
        <h1 class="text-h5 font-weight-bold text-secondary">{{ project.name }}</h1>
        <p class="text-body-2 text-medium-emphasis">{{ project.client }} — {{ project.city }}/{{ project.state }}</p>
      </div>
      <v-spacer />
      <v-btn color="primary" variant="outlined" :to="`/projects/${project.id}/edit`" prepend-icon="mdi-pencil" class="mr-2">
        Editar
      </v-btn>
      <v-chip :color="getStatusColor(project.status)" variant="tonal" size="large">
        {{ project.status }}
      </v-chip>
    </div>

    <!-- Dados Gerais + Risco -->
    <v-row class="mb-6">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold">
            <v-icon start color="primary" size="small">mdi-information</v-icon>
            Dados Gerais
          </v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="6" md="4">
                <p class="text-caption text-medium-emphasis">Tipo de Serviço</p>
                <p class="font-weight-medium">{{ project.service_type }}</p>
              </v-col>
              <v-col cols="6" md="4">
                <p class="text-caption text-medium-emphasis">Responsável</p>
                <p class="font-weight-medium">{{ project.responsible }}</p>
              </v-col>
              <v-col cols="6" md="4">
                <p class="text-caption text-medium-emphasis">Prioridade</p>
                <v-chip :color="getPriorityColor(project.priority)" size="small">{{ project.priority }}</v-chip>
              </v-col>
              <v-col cols="6" md="4">
                <p class="text-caption text-medium-emphasis">Data de Início</p>
                <p class="font-weight-medium">{{ formatDate(project.start_date) }}</p>
              </v-col>
              <v-col cols="6" md="4">
                <p class="text-caption text-medium-emphasis">Previsão de Conclusão</p>
                <p class="font-weight-medium">{{ formatDate(project.expected_end_date) }}</p>
              </v-col>
              <v-col cols="6" md="4">
                <p class="text-caption text-medium-emphasis">Conclusão Real</p>
                <p class="font-weight-medium">{{ project.actual_end_date ? formatDate(project.actual_end_date) : '—' }}</p>
              </v-col>
              <v-col cols="12" v-if="project.technical_notes">
                <p class="text-caption text-medium-emphasis">Observações Técnicas</p>
                <p class="font-weight-medium">{{ project.technical_notes }}</p>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card :class="{ 'border-error': risk.risk_level === 'Alto' }">
          <v-card-title class="text-subtitle-1 font-weight-bold">
            <v-icon start color="warning" size="small">mdi-alert-decagram</v-icon>
            Análise de Risco
          </v-card-title>
          <v-card-text class="text-center">
            <div class="risk-score-circle mb-3" :class="`risk-${risk.risk_level?.toLowerCase()}`">
              <span class="text-h4 font-weight-bold">{{ risk.risk_score }}%</span>
              <span class="text-caption d-block">Risco de Atraso</span>
            </div>
            <v-chip :color="getRiskColor(risk.risk_level)" size="large" class="mb-3">
              {{ risk.risk_level }}
            </v-chip>
            <div class="text-left mt-3" v-if="risk.risk_factors && risk.risk_factors.length">
              <p class="text-caption text-medium-emphasis mb-2 font-weight-bold">Fatores de Risco:</p>
              <div v-for="(factor, idx) in risk.risk_factors" :key="idx" class="mb-1">
                <v-icon size="x-small" color="warning" class="mr-1">mdi-alert</v-icon>
                <span class="text-caption">{{ factor }}</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Indicadores de Custo e Prazo -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold">
            <v-icon start color="primary" size="small">mdi-currency-brl</v-icon>
            Indicadores de Custo
          </v-card-title>
          <v-card-text>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-body-2">Custo Estimado</span>
              <span class="font-weight-bold">{{ formatCurrency(project.estimated_cost) }}</span>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-body-2">Custo Realizado</span>
              <span class="font-weight-bold" :class="costOverrun > 0 ? 'text-error' : 'text-success'">
                {{ formatCurrency(project.actual_cost) }}
              </span>
            </div>
            <v-divider class="my-2" />
            <div class="d-flex justify-space-between">
              <span class="text-body-2">Desvio</span>
              <v-chip :color="costOverrun > 10 ? 'error' : costOverrun > 0 ? 'warning' : 'success'" size="small">
                {{ costOverrun > 0 ? '+' : '' }}{{ costOverrun.toFixed(1) }}%
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="Math.min((project.actual_cost / project.estimated_cost) * 100, 150)"
              :color="costOverrun > 10 ? 'error' : costOverrun > 0 ? 'warning' : 'success'"
              height="8"
              rounded
              class="mt-3"
            />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold">
            <v-icon start color="primary" size="small">mdi-calendar-clock</v-icon>
            Indicadores de Prazo
          </v-card-title>
          <v-card-text>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-body-2">Duração Prevista</span>
              <span class="font-weight-bold">{{ plannedDuration }} dias</span>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-body-2">Dias Decorridos</span>
              <span class="font-weight-bold">{{ elapsedDays }} dias</span>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-body-2">Dias Restantes</span>
              <span class="font-weight-bold" :class="remainingDays < 0 ? 'text-error' : ''">
                {{ remainingDays }} dias
              </span>
            </div>
            <v-progress-linear
              :model-value="Math.min((elapsedDays / plannedDuration) * 100, 100)"
              :color="remainingDays < 0 ? 'error' : remainingDays < 15 ? 'warning' : 'primary'"
              height="8"
              rounded
              class="mt-3"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Linha do Tempo das Etapas -->
    <v-card class="mb-6">
      <v-card-title class="text-subtitle-1 font-weight-bold">
        <v-icon start color="primary" size="small">mdi-timeline</v-icon>
        Linha do Tempo das Etapas
      </v-card-title>
      <v-card-text>
        <v-timeline side="end" density="compact">
          <v-timeline-item
            v-for="(stage, idx) in stageTimeline"
            :key="idx"
            :dot-color="stage.color"
            :icon="stage.icon"
            size="small"
          >
            <div class="d-flex align-center">
              <div>
                <p class="font-weight-bold text-body-2">{{ stage.stage }}</p>
                <p class="text-caption text-medium-emphasis">
                  {{ formatDate(stage.started_at) }}
                  <span v-if="stage.completed_at"> — {{ formatDate(stage.completed_at) }}</span>
                  <span v-if="stage.days_in_stage"> ({{ stage.days_in_stage }} dias)</span>
                </p>
              </div>
              <v-spacer />
              <v-chip v-if="stage.isCurrent" color="primary" size="x-small">Atual</v-chip>
              <v-chip v-else-if="stage.completed_at" color="success" size="x-small" variant="tonal">Concluída</v-chip>
            </div>
          </v-timeline-item>
        </v-timeline>
      </v-card-text>
    </v-card>
  </div>

  <!-- Loading -->
  <div v-else class="d-flex justify-center align-center" style="min-height: 400px;">
    <v-progress-circular indeterminate color="primary" size="64" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api.js'

const route = useRoute()
const project = ref(null)
const risk = ref({ risk_score: 0, risk_level: 'Baixo', risk_factors: [] })
const history = ref([])

const costOverrun = computed(() => {
  if (!project.value || !project.value.estimated_cost) return 0
  return ((project.value.actual_cost - project.value.estimated_cost) / project.value.estimated_cost) * 100
})

const plannedDuration = computed(() => {
  if (!project.value) return 0
  const start = new Date(project.value.start_date)
  const end = new Date(project.value.expected_end_date)
  return Math.ceil((end - start) / (1000 * 60 * 60 * 24))
})

const elapsedDays = computed(() => {
  if (!project.value) return 0
  const start = new Date(project.value.start_date)
  const now = new Date()
  return Math.ceil((now - start) / (1000 * 60 * 60 * 24))
})

const remainingDays = computed(() => {
  if (!project.value) return 0
  const end = new Date(project.value.expected_end_date)
  const now = new Date()
  return Math.ceil((end - now) / (1000 * 60 * 60 * 24))
})

const stageTimeline = computed(() => {
  const allStages = ['Orçamento', 'Projeto técnico', 'Produção', 'Pré-montagem', 'Expedição', 'Instalação', 'Finalizado']
  return history.value.map(h => {
    const isCurrent = h.stage === project.value?.current_stage && !h.completed_at
    return {
      ...h,
      isCurrent,
      color: isCurrent ? 'primary' : h.completed_at ? 'success' : 'grey',
      icon: isCurrent ? 'mdi-play-circle' : h.completed_at ? 'mdi-check-circle' : 'mdi-circle-outline',
    }
  })
})

function getStatusColor(status) {
  const colors = { 'Em andamento': 'info', 'Finalizado': 'success', 'Atrasado': 'error', 'Pausado': 'warning' }
  return colors[status] || 'grey'
}

function getPriorityColor(priority) {
  const colors = { 'Crítica': 'error', 'Alta': 'warning', 'Média': 'info', 'Baixa': 'success' }
  return colors[priority] || 'grey'
}

function getRiskColor(level) {
  const colors = { 'Alto': 'error', 'Médio': 'warning', 'Baixo': 'success' }
  return colors[level] || 'grey'
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 0 }).format(value)
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('pt-BR')
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [projectRes, historyRes, riskRes] = await Promise.all([
      api.get(`/projects/${id}`),
      api.get(`/projects/${id}/history`),
      api.get(`/projects/${id}/risk`),
    ])
    project.value = projectRes.data
    history.value = historyRes.data
    risk.value = riskRes.data
  } catch (error) {
    console.error('Erro ao carregar projeto:', error)
  }
})
</script>

<style scoped>
.risk-score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  border: 4px solid;
}
.risk-baixo { border-color: #388E3C; color: #388E3C; }
.risk-médio { border-color: #F57C00; color: #F57C00; }
.risk-alto { border-color: #D32F2F; color: #D32F2F; }
.border-error { border: 2px solid #D32F2F !important; }
</style>
