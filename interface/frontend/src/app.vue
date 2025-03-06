<template>
    <div id="app">
      <h1>Interactive Sound Art Controller</h1>
      <!-- Gebruik de SettingsComponent en geef de gewenste boxId door -->
      <SettingsComponent :boxId="'box1'" />
    </div>
  </template>
  
  <script setup>
  import SettingsComponent from './components/SettingsComponent.vue';
  </script>
  
  <style>
  /* Globale stijlen voor de app */
  #app {
    text-align: center;
    margin: 20px;
  }
  </style>
  