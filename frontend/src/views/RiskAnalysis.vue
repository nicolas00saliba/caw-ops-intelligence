<template>
  <div>
    <div class="d-flex align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-secondary">Análise de Risco Operacional</h1>
        <p class="text-body-2 text-medium-emphasis">Inteligência preditiva para gestão de atrasos</p>
      </div>
      <v-spacer />
      <v-chip color="warning" variant="tonal" size="large">
        <v-icon start>mdi-brain</v-icon>
        Motor de Risco v1.0
      </v-chip>
    </div>

    <!-- Resumo de Risco -->
    <v-row class="mb-6">
      <v-col cols="12" md="4">
        <v-card color="error" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-avatar color="error" size="48" class="mr-4">
              <v-icon color="white">mdi-alert-octagon</v-icon>
            </v-avatar>
            <div>
              <p class="text-h4 font-weight-bold text-error">{{ riskSummary.high }}</p>
              <p class="text-caption">Risco Alto</p>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="warning" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-avatar color="warning" size="48" class="mr-4">
              <v-icon color="white">mdi-alert</v-icon>
            </v-avatar>
            <div>
              <p class="text-h4 font-weight-bold text-warning">{{ riskSummary.medium }}</p>
              <p class="text-caption">Risco Médio</p>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="success" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-avatar color="success" size="48" class="mr-4">
              <v-icon color="white">mdi-check-circle</v-icon>
            </v-avatar>
            <div>
              <p class="text-h4 font-weight-bold text-success">{{ riskSummary.low }}</p>
              <p class="text-caption">Risco Baixo</p>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Explicação do Motor -->
    <v-card class="mb-6" variant="outlined">
      <v-card-text class="pa-4">
        <div class="d-flex align-center mb-2">
          <v-icon color="primary" class="mr-2">mdi-information</v-icon>
          <span class="font-weight-bold text-secondary">Como funciona o Motor de Risco</span>
        </div>
        <p class="text-body-2 text-medium-emphasis">
          O score de risco é calculado com base em 6 fatores ponderados: estagnação na etapa atual (25%),
          proximidade do prazo de vencimento (25%), desvio de custo (20%), complexidade do serviço (15%),
          histórico de atrasos em serviços semelhantes (10%) e prioridade do projeto (5%).
          O resultado é um percentual de 0 a 100% que indica a probabilidade de atraso.
        </p>
      </v-card-text>
    </v-card>

    <!-- Lista de Projetos com Risco -->
    <v-card>
      <v-card-title class="d-flex align-center pa-4">
        <v-icon color="primary" class="mr-2">mdi-format-list-checks</v-icon>
        <span class="text-subtitle-1 font-weight-bold">Projetos Ativos — Ordenados por Risco</span>
        <v-spacer />
        <v-text-field
          v-model="searchRisk"
          label="Filtrar..."
          prepend-inner-icon="mdi-magnify"
          hide-details
          density="compact"
          style="max-width: 250px;"
          clearable
        />
      </v-card-title>

      <v-divider />

      <div v-if="loading" class="d-flex justify-center pa-8">
        <v-progress-circular indeterminate color="primary" />
      </div>

      <v-list v-else lines="three" class="pa-0">
        <template v-for="(item, idx) in filteredRiskItems" :key="item.project_id">
          <v-list-item class="pa-4" :to="`/projects/${item.project_id}`">
            <template v-slot:prepend>
              <div class="risk-badge mr-4" :class="`risk-badge--${item.risk_level.toLowerCase()}`">
                <span class="text-h6 font-weight-bold">{{ item.risk_score.toFixed(0) }}%</span>
              </div>
            </template>

            <v-list-item-title class="font-weight-bold mb-1">
              {{ item.project_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="mb-2">
              <v-chip size="x-small" class="mr-1">{{ item.service_type }}</v-chip>
              <v-chip size="x-small" class="mr-1">{{ item.city }}/{{ item.state }}</v-chip>
              <v-chip size="x-small">{{ item.current_stage }}</v-chip>
            </v-list-item-subtitle>

            <div class="d-flex flex-wrap gap-1">
              <v-chip
                v-for="(factor, fIdx) in item.risk_factors.slice(0, 3)"
                :key="fIdx"
                size="x-small"
                color="warning"
                variant="tonal"
              >
                <v-icon start size="x-small">mdi-alert</v-icon>
                {{ factor }}
              </v-chip>
            </div>

            <template v-slot:append>
              <div class="text-right">
                <v-chip :color="getRiskColor(item.risk_level)" size="small" class="mb-1">
                  {{ item.risk_level }}
                </v-chip>
                <div v-if="item.days_delayed > 0" class="text-caption text-error">
                  {{ item.days_delayed }} dias atrasado
                </div>
                <div v-if="item.cost_overrun_pct > 0" class="text-caption text-warning">
                  +{{ item.cost_overrun_pct.toFixed(0) }}% custo
                </div>
              </div>
            </template>
          </v-list-item>
          <v-divider v-if="idx < filteredRiskItems.length - 1" />
        </template>
      </v-list>

      <v-card-text v-if="!loading && filteredRiskItems.length === 0" class="text-center pa-8">
        <v-icon size="64" color="grey-lighten-1">mdi-check-decagram</v-icon>
        <p class="text-h6 text-medium-emphasis mt-2">Nenhum projeto com risco encontrado</p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api.js'

const riskItems = ref([])
const loading = ref(true)
const searchRisk = ref('')

const riskSummary = computed(() => {
  return {
    high: riskItems.value.filter(i => i.risk_level === 'Alto').length,
    medium: riskItems.value.filter(i => i.risk_level === 'Médio').length,
    low: riskItems.value.filter(i => i.risk_level === 'Baixo').length,
  }
})

const filteredRiskItems = computed(() => {
  if (!searchRisk.value) return riskItems.value
  const term = searchRisk.value.toLowerCase()
  return riskItems.value.filter(i =>
    i.project_name.toLowerCase().includes(term) ||
    i.service_type.toLowerCase().includes(term) ||
    i.city.toLowerCase().includes(term)
  )
})

function getRiskColor(level) {
  const colors = { 'Alto': 'error', 'Médio': 'warning', 'Baixo': 'success' }
  return colors[level] || 'grey'
}

onMounted(async () => {
  try {
    const response = await api.get('/projects/risk-analysis')
    riskItems.value = response.data
  } catch (error) {
    console.error('Erro ao carregar análise de risco:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.risk-badge {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid;
}
.risk-badge--alto {
  border-color: #D32F2F;
  color: #D32F2F;
  background: rgba(211, 47, 47, 0.05);
}
.risk-badge--médio {
  border-color: #F57C00;
  color: #F57C00;
  background: rgba(245, 124, 0, 0.05);
}
.risk-badge--baixo {
  border-color: #388E3C;
  color: #388E3C;
  background: rgba(56, 142, 60, 0.05);
}
</style>
