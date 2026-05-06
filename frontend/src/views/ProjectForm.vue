<template>
  <div>
    <div class="d-flex align-center mb-6">
      <v-btn icon variant="text" @click="$router.back()" class="mr-3">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <div>
        <h1 class="text-h5 font-weight-bold text-secondary">
          {{ isEditing ? 'Editar Projeto' : 'Novo Projeto' }}
        </h1>
        <p class="text-body-2 text-medium-emphasis">
          {{ isEditing ? 'Atualize os dados do projeto' : 'Cadastre um novo projeto operacional' }}
        </p>
      </div>
    </div>

    <v-card>
      <v-card-text class="pa-6">
        <v-form ref="formRef" @submit.prevent="handleSubmit">
          <v-row>
            <v-col cols="12" md="8">
              <v-text-field
                v-model="form.name"
                label="Nome do Projeto *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-folder"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.client"
                label="Cliente *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-domain"
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-select
                v-model="form.service_type"
                :items="serviceTypes"
                label="Tipo de Serviço *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-wrench"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.city"
                label="Cidade *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-city"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="form.state"
                :items="states"
                label="Estado *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-map"
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.responsible"
                label="Responsável *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-account"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="form.current_stage"
                :items="stages"
                label="Etapa Atual *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-progress-check"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="form.status"
                :items="statuses"
                label="Status *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-flag"
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-select
                v-model="form.priority"
                :items="priorities"
                label="Prioridade *"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-alert-circle"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.start_date"
                label="Data de Início *"
                type="date"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-calendar-start"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.expected_end_date"
                label="Previsão de Conclusão *"
                type="date"
                :rules="[v => !!v || 'Obrigatório']"
                prepend-inner-icon="mdi-calendar-end"
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.actual_end_date"
                label="Data Real de Conclusão"
                type="date"
                prepend-inner-icon="mdi-calendar-check"
                clearable
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model.number="form.estimated_cost"
                label="Custo Estimado (R$) *"
                type="number"
                :rules="[v => v > 0 || 'Obrigatório']"
                prepend-inner-icon="mdi-currency-brl"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model.number="form.actual_cost"
                label="Custo Realizado (R$)"
                type="number"
                prepend-inner-icon="mdi-cash"
              />
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="form.technical_notes"
                label="Observações Técnicas"
                rows="3"
                prepend-inner-icon="mdi-note-text"
              />
            </v-col>
          </v-row>

          <v-divider class="my-4" />

          <div class="d-flex justify-end gap-3">
            <v-btn variant="outlined" @click="$router.back()">Cancelar</v-btn>
            <v-btn color="primary" type="submit" :loading="saving" prepend-icon="mdi-content-save">
              {{ isEditing ? 'Salvar Alterações' : 'Cadastrar Projeto' }}
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api.js'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const saving = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const isEditing = computed(() => !!route.params.id)

const form = ref({
  name: '',
  client: '',
  service_type: '',
  city: '',
  state: '',
  responsible: '',
  current_stage: 'Orçamento',
  status: 'Em andamento',
  priority: 'Média',
  start_date: new Date().toISOString().split('T')[0],
  expected_end_date: '',
  actual_end_date: null,
  estimated_cost: 0,
  actual_cost: 0,
  technical_notes: '',
})

const serviceTypes = ['Torre Telecom', 'Fundação', 'Poste', 'Reforço Estrutural', 'Subestação', 'Estrutura Metálica', 'Manutenção']
const stages = ['Orçamento', 'Projeto técnico', 'Produção', 'Pré-montagem', 'Expedição', 'Instalação', 'Finalizado']
const statuses = ['Em andamento', 'Finalizado', 'Atrasado', 'Pausado']
const priorities = ['Crítica', 'Alta', 'Média', 'Baixa']
const states = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

async function handleSubmit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.actual_end_date) payload.actual_end_date = null
    if (!payload.actual_cost) payload.actual_cost = 0

    if (isEditing.value) {
      await api.put(`/projects/${route.params.id}`, payload)
      snackbarText.value = 'Projeto atualizado com sucesso!'
    } else {
      await api.post('/projects/', payload)
      snackbarText.value = 'Projeto cadastrado com sucesso!'
    }
    snackbarColor.value = 'success'
    snackbar.value = true
    setTimeout(() => router.push('/projects'), 1500)
  } catch (error) {
    snackbarText.value = 'Erro ao salvar projeto'
    snackbarColor.value = 'error'
    snackbar.value = true
    console.error(error)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (isEditing.value) {
    try {
      const response = await api.get(`/projects/${route.params.id}`)
      const data = response.data
      form.value = {
        name: data.name,
        client: data.client,
        service_type: data.service_type,
        city: data.city,
        state: data.state,
        responsible: data.responsible,
        current_stage: data.current_stage,
        status: data.status,
        priority: data.priority,
        start_date: data.start_date,
        expected_end_date: data.expected_end_date,
        actual_end_date: data.actual_end_date || null,
        estimated_cost: data.estimated_cost,
        actual_cost: data.actual_cost || 0,
        technical_notes: data.technical_notes || '',
      }
    } catch (error) {
      console.error('Erro ao carregar projeto:', error)
    }
  }
})
</script>
