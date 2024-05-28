<script setup lang="ts">
import { PropType } from 'vue';

const props = defineProps({
  totals: {
    type: Object as PropType<{ passed: number; failed: number; pending: number }>,
    required: true,
  },
});

</script>

<template>
  <div class="flex items-center justify-center">
    <div class="max-w-sm w-full bg-secondary rounded-lg shadow-lg p-5 text-left">
      <h2 class="text-lg font-bold text-primary mb-4">Overall Test Results</h2>
      <p class="text-success font-semibold">Passed: {{ totals.passed }}</p>
      <p class="text-error font-semibold">Failed: {{ totals.failed }}</p>
      <p class="text-warning font-semibold">Pending: {{ totals.pending }}</p>
    </div>
  </div>
</template>


<style scoped>
</style>
