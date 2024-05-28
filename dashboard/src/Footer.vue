<script setup lang="ts">
const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="bg-primary text-secondary text-center p-2">
    <p class="text-sm">© <span id="current-copyright-year">{{ currentYear }}</span> Dashboard, Inc.</p>
  </footer>
</template>


<style scoped>
</style>
