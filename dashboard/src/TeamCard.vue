<script setup lang="ts">
import { Team } from '@/App.vue';
import { PropType } from 'vue';

const props = defineProps({
  team: {
    type: Object as PropType<Team>,
    required: true,
  },
});
</script>

<template>
  <div class="bg-secondary rounded-lg shadow-lg p-4 m-2">
    <h3 class="text-primary font-bold">{{ team.name }}</h3>
    <p class="text-success">Passed: {{ team.totals.passing }}</p>
    <p class="text-error">Failed: {{ team.totals.failing }}</p>
    <p class="text-warning">Pending: {{ team.totals.pending }}</p>
  </div>
</template>

<style scoped>
</style>
