<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';

// Реактивний об'єкт для зберігання даних з форм
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

// Реактивні змінні для стану інтерфейсу
const result = ref(null);
const isLoading = ref(false);
const errorMessage = ref('');
const showInfoModal = ref(false); // Для модального вікна "Інфо"

// Функція, яка викликається при натисканні на кнопку
async function performCalculation() {
  isLoading.value = true;
  errorMessage.value = '';
  result.value = null;
  try {
    const response = await axios.post('/api/calculate', params);
    result.value = response.data;
  } catch (error) {
    errorMessage.value = 'Помилка сервера розрахунків. Перевірте, чи він запущений.';
    console.error(error);
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div id="app-container">

    <header class="main-header">
      <div class="header-top-line">
        <div class="logo-info-group">
          <span class="logo">The Ravens</span>
          <a href="#" @click.prevent="showInfoModal = true" class="info-btn" title="Інформація">ⓘ</a>
        </div>
      </div>
      <nav class="header-nav">
        <a href="#" class="active">Головна</a>
        <a href="#">Генератор</a>
        <a href="#">Характеристики</a>
        <a href="#">Підтримка</a>
      </nav>
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
      
      </main>
  </div>

  <div v-if="result || errorMessage" class="modal" @click.self="result = null; errorMessage = ''">
      <div class="modal-content">
          <button @click="result = null; errorMessage = ''" class="close-button">&times;</button>
          <h2>Результат з сервера</h2>
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          <div v-if="result" class="result-content">
              <p>Максимальна дальність: <strong>{{ result.flightDistance_km }} км</strong></p>
              <p>Час польоту: <strong>{{ result.flightTime_min }} хв</strong></p>
              <p>Швидкість відносно повітря: <strong>{{ result.airSpeed_ms }} м/с</strong></p>
              <p>Загальна потужність: <strong>{{ result.totalPower_W }} Вт</strong></p>
          </div>
      </div>
  </div>

  <div v-if="showInfoModal" class="modal" @click.self="showInfoModal = false">
      <div class="modal-content">
          <button @click="showInfoModal = false" class="close-button">&times;</button>
          <h2 class="team-title">The Ravens TEAM</h2>
          <p>ver. :0.0.1</p>
          <p>By: Goodbye & Alik</p>
      </div>
  </div>
</template>

<style>
/* ОСНОВНІ СТИЛІ */
:root { 
    --background-color: #1c1c1f; 
    --control-block-bg: #252528; 
    --text-color: #e0e0e0; 
    --text-color-muted: #888;
    --primary-color: #00aaff; 
    --border-color: #444; 
    --accent-color: #e74c3c;
}
body { 
    margin: 0; 
    background-color: var(--background-color); 
    color: var(--text-color); 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
#app-container { 
    max-width: 600px; 
    margin: 0 auto; 
    padding: 0 15px 20px 15px;
}

/* СТИЛІ ДЛЯ НОВОЇ ШАПКИ */
.main-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px 0;
    margin-bottom: 20px;
}
.header-top-line {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.logo-info-group {
    display: flex;
    align-items: center;
    gap: 20px;
}
.logo {
    font-size: 1.8em;
    font-weight: bold;
    color: var(--text-color);
}
.info-btn {
    font-size: 1.5em;
    font-weight: bold;
    color: var(--text-color-muted);
    text-decoration: none;
    transition: color 0.3s;
}
.info-btn:hover {
    color: var(--primary-color);
}
.header-nav {
    display: flex;
    justify-content: center;
    gap: 15px;
    width: 100%;
    margin-top: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-color);
}
.header-nav a {
    color: var(--text-color-muted);
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 6px;
    transition: background-color 0.3s, color 0.3s;
}
.header-nav a:hover {
    background-color: var(--control-block-bg);
    color: var(--text-color);
}
.header-nav a.active {
    color: var(--primary-color);
    font-weight: bold;
}

/* СТИЛІ КОНТЕНТУ */
.params-block, .result-block { background: var(--control-block-bg); padding: 20px; border-radius: 12px; margin-bottom: 20px; }
.input-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.input-group label { display: block; font-size: 0.9em; margin-bottom: 5px; color: #888; }
.input-group input { width: 100%; box-sizing: border-box; padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; background-color: #2a2a2e; color: var(--text-color); font-size: 1em; }
.calculate-wrapper { text-align: center; }
button { width: 100%; padding: 15px; font-size: 1.2em; border: none; border-radius: 8px; background-color: var(--accent-color); color: white; cursor: pointer; transition: background-color 0.3s; }
button:disabled { background-color: #555; cursor: not-allowed; }
.error-message { color: var(--accent-color); text-align: center; font-weight: bold; }

/* ПОКРАЩЕНІ СТИЛІ ДЛЯ МОДАЛЬНОГО ВІКНА */
.modal {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
    box-sizing: border-box;
}
.modal-content {
    background-color: var(--control-block-bg);
    padding: 25px;
    border: 1px solid var(--border-color);
    width: 100%;
    max-width: 500px;
    border-radius: 12px;
    position: relative;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    max-height: 90vh;
    overflow-y: auto;
}
.close-button {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    color: #aaa;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    padding: 0;
    width: auto;
}
.close-button:hover { color: white; }
.result-content { margin-top: 15px; }
.result-content p { margin: 10px 0; }
.result-content strong { color: var(--primary-color); }
.team-title { color: var(--primary-color); text-align: center; }
</style>