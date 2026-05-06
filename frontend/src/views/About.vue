<template>
  <div>
    <div class="d-flex align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-secondary">Sobre o Sistema</h1>
        <p class="text-body-2 text-medium-emphasis">CAW Ops Intelligence — Inteligência Operacional</p>
      </div>
    </div>

    <!-- Objetivo -->
    <v-card class="mb-6">
      <v-card-text class="pa-6">
        <div class="d-flex align-center mb-4">
          <v-avatar color="primary" size="48" class="mr-4">
            <v-icon color="white">mdi-target</v-icon>
          </v-avatar>
          <h2 class="text-h6 font-weight-bold text-secondary">Objetivo</h2>
        </div>
        <p class="text-body-1 text-medium-emphasis">
          O <strong>CAW Ops Intelligence</strong> é um sistema de gestão operacional e inteligência de risco
          desenvolvido para empresas de infraestrutura de telecomunicações e energia. Seu objetivo é centralizar
          o acompanhamento de projetos, identificar riscos de atraso de forma preditiva e fornecer indicadores
          gerenciais que apoiem a tomada de decisão.
        </p>
      </v-card-text>
    </v-card>

    <!-- Problema que resolve -->
    <v-card class="mb-6">
      <v-card-text class="pa-6">
        <div class="d-flex align-center mb-4">
          <v-avatar color="error" size="48" class="mr-4">
            <v-icon color="white">mdi-alert-circle</v-icon>
          </v-avatar>
          <h2 class="text-h6 font-weight-bold text-secondary">Problema Operacional</h2>
        </div>
        <p class="text-body-1 text-medium-emphasis mb-3">
          Empresas como a CAW Telecom e Energia gerenciam simultaneamente dezenas de projetos de infraestrutura
          em diferentes cidades e estados. Sem um sistema integrado, é comum enfrentar:
        </p>
        <v-list density="compact">
          <v-list-item prepend-icon="mdi-close-circle" class="text-body-2">
            Falta de visibilidade sobre o status real de cada projeto
          </v-list-item>
          <v-list-item prepend-icon="mdi-close-circle" class="text-body-2">
            Dificuldade em identificar projetos com risco de atraso antes que se tornem críticos
          </v-list-item>
          <v-list-item prepend-icon="mdi-close-circle" class="text-body-2">
            Controle de custos fragmentado em planilhas desconectadas
          </v-list-item>
          <v-list-item prepend-icon="mdi-close-circle" class="text-body-2">
            Ausência de indicadores gerenciais consolidados para tomada de decisão
          </v-list-item>
          <v-list-item prepend-icon="mdi-close-circle" class="text-body-2">
            Histórico de etapas não rastreável, dificultando análises de desempenho
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <!-- Como ajuda -->
    <v-card class="mb-6">
      <v-card-text class="pa-6">
        <div class="d-flex align-center mb-4">
          <v-avatar color="success" size="48" class="mr-4">
            <v-icon color="white">mdi-check-decagram</v-icon>
          </v-avatar>
          <h2 class="text-h6 font-weight-bold text-secondary">Como Ajuda a CAW</h2>
        </div>
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4 h-100">
              <v-icon color="primary" class="mb-2">mdi-view-dashboard</v-icon>
              <h3 class="text-subtitle-2 font-weight-bold mb-1">Dashboard Gerencial</h3>
              <p class="text-caption text-medium-emphasis">
                Visão consolidada de todos os projetos, custos e indicadores em tempo real.
              </p>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4 h-100">
              <v-icon color="warning" class="mb-2">mdi-alert-decagram</v-icon>
              <h3 class="text-subtitle-2 font-weight-bold mb-1">Análise de Risco Preditiva</h3>
              <p class="text-caption text-medium-emphasis">
                Identificação antecipada de projetos com probabilidade de atraso, com explicação dos fatores.
              </p>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4 h-100">
              <v-icon color="info" class="mb-2">mdi-timeline</v-icon>
              <h3 class="text-subtitle-2 font-weight-bold mb-1">Rastreabilidade de Etapas</h3>
              <p class="text-caption text-medium-emphasis">
                Histórico completo de cada etapa do projeto, com tempo de permanência e gargalos.
              </p>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4 h-100">
              <v-icon color="secondary" class="mb-2">mdi-cash-multiple</v-icon>
              <h3 class="text-subtitle-2 font-weight-bold mb-1">Controle de Custos</h3>
              <p class="text-caption text-medium-emphasis">
                Comparação entre custo previsto e realizado, com alertas de desvio por projeto e tipo de serviço.
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Tecnologias -->
    <v-card class="mb-6">
      <v-card-text class="pa-6">
        <div class="d-flex align-center mb-4">
          <v-avatar color="info" size="48" class="mr-4">
            <v-icon color="white">mdi-code-braces</v-icon>
          </v-avatar>
          <h2 class="text-h6 font-weight-bold text-secondary">Tecnologias Utilizadas</h2>
        </div>
        <v-row>
          <v-col cols="12" md="4">
            <h3 class="text-subtitle-2 font-weight-bold mb-2 text-primary">Frontend</h3>
            <v-chip class="mr-1 mb-1" size="small">Vue 3</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Vite</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Vuetify 3</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Vue Router</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Axios</v-chip>
            <v-chip class="mr-1 mb-1" size="small">ApexCharts</v-chip>
          </v-col>
          <v-col cols="12" md="4">
            <h3 class="text-subtitle-2 font-weight-bold mb-2 text-primary">Backend</h3>
            <v-chip class="mr-1 mb-1" size="small">Python</v-chip>
            <v-chip class="mr-1 mb-1" size="small">FastAPI</v-chip>
            <v-chip class="mr-1 mb-1" size="small">SQLAlchemy</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Pydantic</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Uvicorn</v-chip>
            <v-chip class="mr-1 mb-1" size="small">SQLite</v-chip>
          </v-col>
          <v-col cols="12" md="4">
            <h3 class="text-subtitle-2 font-weight-bold mb-2 text-primary">Dados / IA</h3>
            <v-chip class="mr-1 mb-1" size="small">Pandas</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Scikit-learn</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Motor de Regras</v-chip>
            <v-chip class="mr-1 mb-1" size="small">Score Ponderado</v-chip>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Evoluções Futuras -->
    <v-card>
      <v-card-text class="pa-6">
        <div class="d-flex align-center mb-4">
          <v-avatar color="secondary" size="48" class="mr-4">
            <v-icon color="white">mdi-rocket-launch</v-icon>
          </v-avatar>
          <h2 class="text-h6 font-weight-bold text-secondary">Evoluções Futuras</h2>
        </div>
        <v-row>
          <v-col cols="12" md="6">
            <v-list density="compact">
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Integração com ERP corporativo</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Autenticação com permissões por perfil (RBAC)</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Migração para PostgreSQL em produção</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Deploy em nuvem (AWS/GCP/Azure)</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Módulo de Business Intelligence (BI)</v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" md="6">
            <v-list density="compact">
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Alertas automáticos por e-mail/SMS</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Integração com dados de campo (IoT)</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Aplicativo mobile para equipes externas</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Machine Learning para previsão de atrasos</v-list-item>
              <v-list-item prepend-icon="mdi-check" class="text-body-2">Relatórios PDF automatizados</v-list-item>
            </v-list>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Footer -->
    <v-card class="mt-6" color="secondary" dark>
      <v-card-text class="text-center pa-6">
        <img src="/caw-logo.png" alt="CAW" style="max-width: 150px; filter: brightness(0) invert(1); opacity: 0.8;" class="mb-3" />
        <p class="text-body-2 text-white" style="opacity: 0.8;">
          CAW Ops Intelligence — Sistema de Gestão Operacional e Inteligência de Risco
        </p>
        <p class="text-caption text-white" style="opacity: 0.5;">
          Desenvolvido como protótipo de sistema corporativo para a CAW Telecom e Energia
        </p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
</script>
