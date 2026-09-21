<template>
  <div id="reconstructed-app-root">
    <router-view v-if="hasRouter" />
    <div v-else class="candidate-shell">
      <h1>Cloud Phone (Candidate Source Shell)</h1>
      <p>Parallel candidate pipeline initialized on port 3112.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const hasRouter = ref(false);
</script>

<style scoped>
.candidate-shell {
  padding: 24px;
  color: #fff;
  background-color: #1a1a1a;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
