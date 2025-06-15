<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';

const params = reactive({
  droneWeight: 1.5,
  payloadWeight: 0.5,
  batteryWeight: 0.8,
  batteryCapacityMAh: 10000,
  groundSpeed_ms: 15,
  windSpeed_ms: 5,
  droneAngle_deg: 0,
  windAngle_deg: 270,
});

const result = ref(null);
const isLoading = ref(false);
const errorMessage = ref('');

async function performCalculation() {
  isLoading.value = true;
  errorMessage.value = '';
  result.value = null;
  try {
    // ВАЖЛИВО: адреса тепер відносна! Vercel сам знайде нашу функцію.
    const response = await axios.post('/api/calculate', params);
    result.value = response.data;
  } catch (error) {
    errorMessage.value = 'Помилка сервера розрахунків.';
    console.error(error);
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div id="app-container">
    <header>
      <h1>The Ravens (Cloud Version)</h1>
    </header>
    <main>
      <section class="params-block">
        <h2>Параметри</h2>
        <div class="input-grid">
            <div class="input-group"><label>Вага дрона, кг</label><input type="number" v-model.number="params.droneWeight"></div>
            <div class="input-group"><label>Вага вантажу, кг</label><input type="number" v-model.number="params.payloadWeight"></div>
            <div class="input-group"><label>Вага АКБ, кг</label><input type="number" v-model.number="params.batteryWeight"></div>
            <div class="input-group"><label>Ємність АКБ, mAh</label><input type="number" v-model.number="params.batteryCapacityMAh"></div>
            <div class="input-group"><label>Швидкість дрона, м/с</label><input type="number" v-model.number="params.groundSpeed_ms"></div>
            <div class="input-group"><label>Швидкість вітру, м/с</label><input type="number" v-model.number="params.windSpeed_ms"></div>
            <div class="input-group"><label>Напрямок дрона, °</label><input type="number" v-model.number="params.droneAngle_deg"></div>
            <div class="input-group"><label>Напрямок вітру, °</label><input type="number" v-model.number="params.windAngle_deg"></div>
        </div>
      </section>

      <div class="calculate-wrapper">
        <button @click="performCalculation" :disabled="isLoading">
          {{ isLoading ? 'Обчислення...' : 'Обчислити у хмарі' }}
        </button>
      </div>

      <section v-if="result || errorMessage" class="result-block">
        <h2>Результат з сервера</h2>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="result" class="result-content">
          <p>Максимальна дальність: <strong>{{ result.flightDistance_km }} км</strong></p>
          <p>Час польоту: <strong>{{ result.flightTime_min }} хв</strong></p>
        </div>
      </section>
    </main>
  </div>
</template>

<style>
/* Тут ті ж самі стилі, що і в попередній версії */
:root { --background-color: #1c1c1f; --control-block-bg: #252528; --text-color: #e0e0e0; --primary-color: #00aaff; --border-color: #444; }
body { margin: 0; background-color: var(--background-color); color: var(--text-color); font-family: sans-serif; }
#app-container { max-width: 600px; margin: 0 auto; padding: 20px; }
header h1 { text-align: center; }
.params-block, .result-block { background: var(--control-block-bg); padding: 20px; border-radius: 12px; margin-bottom: 20px; }
.input-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.input-group label { display: block; font-size: 0.9em; margin-bottom: 5px; color: #888; }
.input-group input { width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; background-color: #2a2a2e; color: var(--text-color); font-size: 1em; }
.calculate-wrapper { text-align: center; }
button { width: 100%; padding: 15px; font-size: 1.2em; border: none; border-radius: 8px; background-color: #e74c3c; color: white; cursor: pointer; }
button:disabled { background-color: #555; }
.result-content p { margin: 10px 0; }
.result-content strong { color: var(--primary-color); }
.error-message { color: #e74c3c; text-align: center; }
</style>