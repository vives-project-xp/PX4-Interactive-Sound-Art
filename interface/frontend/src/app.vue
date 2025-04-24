<template>
  <div id="app">
    <MusicBoxSelector />
  </div>
</template>

<script>
import MusicBoxSelector from "./components/MusicBoxSelector.vue";

export default {
  components: {
    MusicBoxSelector,
  },
};
</script>

<style>
/* Dark Mode Background */
#app {
  font-family: "Arial", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #1e1e1e, #3a3a3a);
}
</style>
