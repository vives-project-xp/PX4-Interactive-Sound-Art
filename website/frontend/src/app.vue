<template>
  <div id="app" :class="{'dark-theme': isDarkMode, 'light-theme': !isDarkMode}">
    <MusicBoxSelector />
  </div>
</template>

<script>
import MusicBoxSelector from "./components/MusicBoxSelector.vue";

export default {
  name: "App",
  components: {
    MusicBoxSelector,
  },
  data() {
    return {
      isDarkMode: false,
    };
  },
  mounted() {
    // Check system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    this.isDarkMode = prefersDark;

    // Listen for changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      this.isDarkMode = e.matches;
    });
  },
};
</script>

<style>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s ease;
}

.dark-theme {
  background-color: #1a1a1a;
}

.light-theme {
  background-color: #ffffff;
}
</style>