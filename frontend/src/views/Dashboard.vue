<template>
  <div>
    <div class="d-flex align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-secondary">Dashboard</h1>
        <p class="text-body-2 text-medium-emphasis">Visão geral da operação — CAW Telecom e Energia</p>
      </div>
      <v-spacer />
      <v-chip color="success" variant="tonal">
        <v-icon start size="small">mdi-circle</v-icon>
        Sistema Online
      </v-chip>
    </div>

    <!-- Cards de Estatísticas -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="4" lg="2">
        <stat-card
          title="Total de Projetos"
          :value="stats.total_projects"
          icon="mdi-folder-multiple"
          color="primary"
        />
      </v-col>
      <v-col cols="12" sm="6" md="4" lg="2">
        <stat-card
          title="Em Andamento"
          :value="stats.in_progress"
          icon="mdi-progress-clock"
          color="info"
        />
      </v-col>
      <v-col cols="12" sm="6" md="4" lg="2">
        <stat-card
          title="Atrasados"
          :value="stats.delayed"
          icon="mdi-alert-circle"
          color="error"
          :alert="stats.delayed > 0"
        />
      </v-col>
      <v-col cols="12" sm="6" md="4" lg="2">
        <stat-card
          title="Risco Alto"
          :value="stats.high_risk"
          icon="mdi-alert-decagram"
          color="warning"
          :alert="stats.high_risk > 0"
        />
      </v-col>
      <v-col cols="12" sm="6" md="4" lg="2">
        <stat-card
          title="Custo Previsto"
          :value="stats.total_estimated_cost"
          icon="mdi-currency-brl"
          color="secondary"
          format="currency"
        />
      </v-col>
      <v-col cols="12" sm="6" md="4" lg="2">
        <stat-card
          title="Custo Realizado"
          :value="stats.total_actual_cost"
          icon="mdi-cash-check"
          color="accent"
          format="currency"
        />
      </v-col>
    </v-row>

    <!-- Gráficos - Linha 1 -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
            <v-icon start color="primary" size="small">mdi-chart-donut</v-icon>
            Projetos por Status
          </v-card-title>
          <v-card-text>
            <apexchart
              v-if="chartsLoaded"
              type="donut"
              height="300"
              :options="statusChartOptions"
              :series="statusChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
            <v-icon start color="primary" size="small">mdi-chart-bar</v-icon>
            Projetos por Tipo de Serviço
          </v-card-title>
          <v-card-text>
            <apexchart
              v-if="chartsLoaded"
              type="bar"
              height="300"
              :options="serviceTypeChartOptions"
              :series="serviceTypeChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Gráficos - Linha 2 -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
            <v-icon start color="primary" size="small">mdi-clock-alert</v-icon>
            Tempo Médio por Etapa (dias)
          </v-card-title>
          <v-card-text>
            <apexchart
              v-if="chartsLoaded"
              type="bar"
              height="300"
              :options="delayChartOptions"
              :series="delayChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
            <v-icon start color="primary" size="small">mdi-cash-multiple</v-icon>
            Custo Previsto vs. Realizado
          </v-card-title>
          <v-card-text>
            <apexchart
              v-if="chartsLoaded"
              type="bar"
              height="300"
              :options="costChartOptions"
              :series="costChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Gráficos - Linha 3 -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
            <v-icon start color="primary" size="small">mdi-alert-decagram</v-icon>
            Distribuição de Risco
          </v-card-title>
          <v-card-text>
            <apexchart
              v-if="chartsLoaded"
              type="pie"
              height="300"
              :options="riskChartOptions"
              :series="riskChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
            <v-icon start color="primary" size="small">mdi-map-marker-multiple</v-icon>
            Top 10 Cidades
          </v-card-title>
          <v-card-text>
            <apexchart
              v-if="chartsLoaded"
              type="bar"
              height="300"
              :options="cityChartOptions"
              :series="cityChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'
import StatCard from '../components/StatCard.vue'

const stats = ref({
  total_projects: 0,
  in_progress: 0,
  delayed: 0,
  high_risk: 0,
  total_estimated_cost: 0,
  total_actual_cost: 0,
})

const chartsLoaded = ref(false)

// Chart data
const statusChartSeries = ref([])
const statusChartOptions = ref({})
const serviceTypeChartSeries = ref([])
const serviceTypeChartOptions = ref({})
const delayChartSeries = ref([])
const delayChartOptions = ref({})
const costChartSeries = ref([])
const costChartOptions = ref({})
const riskChartSeries = ref([])
const riskChartOptions = ref({})
const cityChartSeries = ref([])
const cityChartOptions = ref({})

const chartColors = ['#F5921B', '#333333', '#1976D2', '#388E3C', '#D32F2F', '#7B1FA2', '#F57C00']

onMounted(async () => {
  try {
    // Carregar estatísticas
    const statsRes = await api.get('/dashboard/stats')
    stats.value = statsRes.data

    // Carregar dados dos gráficos
    const [statusRes, serviceRes, delayRes, costRes, riskRes, cityRes] = await Promise.all([
      api.get('/dashboard/charts/status'),
      api.get('/dashboard/charts/service-type'),
      api.get('/dashboard/charts/avg-delay-by-stage'),
      api.get('/dashboard/charts/cost-comparison'),
      api.get('/dashboard/charts/risk-distribution'),
      api.get('/dashboard/charts/projects-by-city'),
    ])

    // Status chart (donut)
    statusChartSeries.value = statusRes.data.values
    statusChartOptions.value = {
      labels: statusRes.data.labels,
      colors: ['#1976D2', '#388E3C', '#D32F2F', '#F57C00'],
      legend: { position: 'bottom' },
      dataLabels: { enabled: true },
    }

    // Service type chart (bar)
    serviceTypeChartSeries.value = [{ name: 'Projetos', data: serviceRes.data.values }]
    serviceTypeChartOptions.value = {
      xaxis: { categories: serviceRes.data.labels },
      colors: ['#F5921B'],
      plotOptions: { bar: { borderRadius: 6, columnWidth: '60%' } },
      dataLabels: { enabled: false },
    }

    // Delay chart (bar horizontal)
    delayChartSeries.value = [{ name: 'Dias médios', data: delayRes.data.values }]
    delayChartOptions.value = {
      xaxis: { categories: delayRes.data.labels },
      colors: ['#1976D2'],
      plotOptions: { bar: { borderRadius: 4, horizontal: true } },
      dataLabels: { enabled: true },
    }

    // Cost comparison chart (grouped bar)
    costChartSeries.value = [
      { name: 'Custo Previsto', data: costRes.data.estimated },
      { name: 'Custo Realizado', data: costRes.data.actual },
    ]
    costChartOptions.value = {
      xaxis: { categories: costRes.data.labels },
      colors: ['#333333', '#F5921B'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '65%' } },
      dataLabels: { enabled: false },
      yaxis: {
        labels: {
          formatter: (val) => `R$ ${(val / 1000).toFixed(0)}k`,
        },
      },
    }

    // Risk distribution (pie)
    riskChartSeries.value = riskRes.data.values
    riskChartOptions.value = {
      labels: riskRes.data.labels,
      colors: ['#388E3C', '#F57C00', '#D32F2F'],
      legend: { position: 'bottom' },
      dataLabels: { enabled: true },
    }

    // City chart (bar horizontal)
    cityChartSeries.value = [{ name: 'Projetos', data: cityRes.data.values }]
    cityChartOptions.value = {
      xaxis: { categories: cityRes.data.labels },
      colors: ['#333333'],
      plotOptions: { bar: { borderRadius: 4, horizontal: true } },
      dataLabels: { enabled: true },
    }

    chartsLoaded.value = true
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  }
})
</script>
