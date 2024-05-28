<script setup lang="ts">
const props = defineProps<{
  team: {
    name: string;
    testResults: {
      passed: number;
      failed: number;
      pending: number;
    };
  };
}>();
</script>

<template>
  <div class="bg-secondary rounded-lg shadow-lg p-4 m-2">
    <h3 class="text-primary font-bold">{{ team.name }}</h3>
    <p class="text-success">Passed: {{ team.testResults.passed }}</p>
    <p class="text-error">Failed: {{ team.testResults.failed }}</p>
    <p class="text-warning">Pending: {{ team.testResults.pending }}</p>
  </div>
</template>

<style scoped>
</style>
