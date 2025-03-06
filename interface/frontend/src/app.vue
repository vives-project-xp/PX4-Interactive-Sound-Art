<template>
  <div id="app">
    
    
    <!-- MusicBoxSelector Component -->
    <MusicBoxSelector />
    
    <!-- SettingsComponent, pass the desired boxId -->
    <!-- <SettingsComponent :boxId="'box1'" /> -->
  </div>
</template>

<script setup>
import MusicBoxSelector from './components/MusicBoxSelector.vue';
//import SettingsComponent from './components/SettingsComponent.vue';
</script>

<style>
/* Global styles for the app */
#app {
  text-align: center;
  margin: 20px;
  color: #fff;
  background-color: #282c34;
  padding: 20px;
  border-radius: 10px;
  backdrop-filter: blur(10px);
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
}
</style>
