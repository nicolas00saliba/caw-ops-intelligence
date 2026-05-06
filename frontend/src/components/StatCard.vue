<template>
  <v-card class="stat-card" :class="{ 'stat-card--alert': alert }">
    <v-card-text class="d-flex align-center pa-5">
      <v-avatar :color="color" size="56" class="mr-4" rounded="lg">
        <v-icon :icon="icon" color="white" size="28" />
      </v-avatar>
      <div class="flex-grow-1">
        <p class="text-caption text-medium-emphasis text-uppercase font-weight-medium mb-1">
          {{ title }}
        </p>
        <p class="text-h5 font-weight-bold" :class="`text-${textColor || 'secondary'}`">
          {{ formattedValue }}
        </p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  value: [Number, String],
  icon: String,
  color: { type: String, default: 'primary' },
  textColor: { type: String, default: '' },
  alert: { type: Boolean, default: false },
  format: { type: String, default: 'number' },
})

const formattedValue = computed(() => {
  if (props.format === 'currency') {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(props.value)
  }
  if (typeof props.value === 'number') {
    return props.value.toLocaleString('pt-BR')
  }
  return props.value
})
</script>

<style scoped>
.stat-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}
.stat-card--alert {
  border-left: 4px solid #D32F2F;
}
</style>
