<template>
  <div id="app">
    <MusicBoxSelector />
  </div>
</template>

<script setup>
import MusicBoxSelector from './components/MusicBoxSelector.vue';
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
</style>
