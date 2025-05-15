<template>
  <div class="container" :class="{ 'dark-mode': isDarkMode, 'light-mode': !isDarkMode }">
    <h1 class="title">Interactive Sound Art Controller</h1>

    <div class="music-box-list">
      <div
        v-for="box in musicBoxes"
        :key="box.id"
        class="music-box"
        :class="{ 
          selected: selectedBox && selectedBox.id === box.id, 
          off: !box.isOn,
          rainbow: box.isOn && box.effect === 'rainbow'
        }"
        @click="selectBox(box)"
        :style="{
          boxShadow: box.isOn && box.effect !== 'rainbow' ? `0 0 20px ${box.color}` : 'none',
          backgroundColor: getBoxBackground(box)
        }"
      >
        <p class="box-name">{{ box.name }}</p>
        <div class="switch" @click.stop="togglePower(box)">
          <div :class="['slider', { on: box.isOn }]" />
        </div>
      </div>
    </div>

    <div v-if="selectedBox" class="settings-section">
      <h2>Settings for {{ selectedBox.name }}</h2>
      <div class="settings-grid">
        <div class="setting">
          <label>Instrument:</label>
          <select
            class="sound-dropdown"
            v-model="selectedBox.instrument"
            @change="updateInstrument"
          >
            <option
              v-for="sound in availableSounds"
              :key="sound"
              :value="sound"
            >
              {{ sound }}
            </option>
          </select>
        </div>

        <div class="setting">
          <label>Effect:</label>
          <select
            class="effect-dropdown"
            v-model="selectedBox.effect"
            @change="updateEffect"
          >
            <option value="solid">Solid</option>
            <option value="puls">Puls</option>
            <option value="chase">Chase</option>
            <option value="fire">Fire</option>
            <option value="sparkle">Sparkle</option>
            <option value="rainbow">Rainbow</option>
          </select>
        </div>

        <div v-if="selectedBox.effect !== 'rainbow'" class="setting">
          <label>Color:</label>
          <input
            type="color"
            class="color-slider"
            v-model="selectedBox.color"
            @input="updateColor"
          />
        </div>

        <div class="setting">
          <label>Volume: <span>{{ selectedBox.volume }}%</span></label>
          <input
            type="range"
            class="volume-slider"
            min="0"
            max="100"
            v-model="selectedBox.volume"
            @input="updateVolume"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import socketService from "../services/socketService.js";

export default {
  name: "MusicBoxSelector",
  data() {
    return {
      musicBoxes: [],
      selectedBox: null,
      availableSounds: [
        "Gitaar",
        "Drum",
        "Bass jumpy",
        "Bell",
        "Synth Sci-Fi",
        "Synth sharp",
        "Bassline",
      ],
      isDarkMode: false,
    };
  },
  mounted() {
    // Initialize color mode based on system preference
    this.initColorMode();

    // connect to the socket server
    socketService.connect();
    socketService.emit("register", { client: "frontend" });
    socketService.on("connect", () => {
      console.log("[Vue] connected to socket server");
    });
    
    // receive initial list of already-connected boxes
    socketService.on("devices-list", (list) => {
      this.musicBoxes = list.map(({ boxId, ip }) => ({
        id: boxId,
        ip,
        name: `Box ${boxId}`,
        isOn: false,
        color: "#FF0000",
        effect: "solid",
        instrument: "Gitaar",
        volume: 50,
      }));
    });

    // handle updates from any client or Pi
    socketService.on("command", (data) => {
      console.log("[Vue] received command:", data);
      const idx = this.musicBoxes.findIndex((b) => b.id === data.boxId);
      if (idx !== -1) {
        const updated = { ...this.musicBoxes[idx], ...data };
        // reactive in-place replace so all UIs update
        this.musicBoxes.splice(idx, 1, updated);
        if (this.selectedBox && this.selectedBox.id === data.boxId) {
          this.selectedBox = updated;
        }
      }
    });

    // when a new Pi connects  
    socketService.on("device-connected", ({ boxId, ip }) => {
      if (!this.musicBoxes.some((b) => b.id === boxId)) {
        this.musicBoxes.push({
          id: boxId,
          ip,
          name: `Box ${boxId}`,
        
          color: "#ff0000",
          effect: "solid",
          instrument: "Gitaar",
          volume: 50,
        });
      }
    });

    // when a Pi disconnects 
    socketService.on("device-disconnected", ({ boxId }) => {
      this.musicBoxes = this.musicBoxes.filter((b) => b.id !== boxId);
      if (this.selectedBox && this.selectedBox.id === boxId) {
        this.selectedBox = null;
      }
    });
  },
  methods: {
    // Color mode methods
    initColorMode() {
      // Use system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      this.isDarkMode = prefersDark;
      
      // Listen for system preference changes
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        this.isDarkMode = e.matches;
      });
    },
    
    selectBox(box) {
      this.selectedBox = box;
    },
    
    togglePower(box) {
      box.isOn = !box.isOn;
      socketService.emit("update-settings", {
        boxId: box.id,
        settings: { isOn: box.isOn },
      });
    },
    
    updateColor() {
      socketService.emit("update-settings", {
        boxId: this.selectedBox.id,
        settings: { color: this.selectedBox.color },
      });
    },
    
    updateEffect() {
      socketService.emit("update-settings", {
        boxId: this.selectedBox.id,
        settings: { effect: this.selectedBox.effect },
      });
    },
    
    updateInstrument() {
      socketService.emit("update-settings", {
        boxId: this.selectedBox.id,
        settings: { instrument: this.selectedBox.instrument },
      });
    },
    
    updateVolume() {
      socketService.emit("update-settings", {
        boxId: this.selectedBox.id,
        settings: { volume: this.selectedBox.volume },
      });
    },
    
    getBoxBackground(box) {
      if (!box.isOn) return 'transparent';
      if (box.effect === 'rainbow') return 'transparent'; // The rainbow class will handle the background
      return box.color;
    },
  },
};
</script>

<style scoped>
/* Base container styles */
.container {
  max-width: 1200px;
  margin: auto;
  text-align: center;
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(15px);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  transition: all 0.3s ease;
}

/* Dark mode styles */
.dark-mode {
  background: rgba(30, 30, 30, 0.8);
  color: white;
}

/* Light mode styles */
.light-mode {
  background: rgba(240, 240, 240, 0.8);
  color: #333;
}

h1, h2 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(97deg, #0096FF, #BB64FF 42%, #F2416B 74%, #EB7500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.dark-mode .music-box {
  background: rgba(50, 50, 50, 0.3);
  border: 1px solid rgba(0, 255, 255, 0.5);
}

.light-mode .music-box {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(200, 200, 200, 0.5);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.music-box-list {
  display: flex;
  flex-direction: column;
  flex-wrap:wrap;
  gap: 20px;
  justify-content: center;
  margin: 20px 0;
}

.music-box {
  padding: 15px;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.music-box.selected {
  transform: scale(1.05);
}

.dark-mode .music-box.selected {
  box-shadow: 0 0 15px rgba(0, 200, 255, 0.5);
}

.light-mode .music-box.selected {
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.3);
}

.music-box.off {
  opacity: 0.4;
}

.dark-mode .box-name {
  background: rgba(0, 0, 0, 0.6);
  color: white;
}

.light-mode .box-name {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.music-box-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.box-name {
  font-size: 1.2rem;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 5px;
  margin: 10px 0;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  margin-top: 10px;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
}

.slider.on {
  background-color: #2196F3;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px; width: 26px;
  left: 4px; bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.slider.on:before {
  transform: translateX(26px);
}

.dark-mode .settings-section {
  background: rgba(50, 50, 50, 0.3);
  border: 1px solid rgba(0, 255, 255, 0.5);
}

.light-mode .settings-section {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(200, 200, 200, 0.5);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.settings-section {
  margin-top: 20px;
  padding: 20px;
  border-radius: 10px;
}

.settings-grid {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.setting {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.setting label {
  margin-bottom: 5px;
  font-weight: 500;
}

.dark-mode .effect-dropdown,
.dark-mode .sound-dropdown,
.dark-mode .volume-slider {
  background: #2a2a2a;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.light-mode .effect-dropdown,
.light-mode .sound-dropdown,
.light-mode .volume-slider {
  background: #ffffff;
  color: #333;
  border: 1px solid rgba(200, 200, 200, 0.8);
}

.effect-dropdown,
.sound-dropdown {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  font-size: 1em;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 8px top 50%;
  background-size: 12px auto;
}

.volume-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  -webkit-appearance: none;
  appearance: none;
  outline: none;
}

.dark-mode .volume-slider {
  background: #555;
}

.light-mode .volume-slider {
  background: #ddd;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  cursor: pointer;
}

.dark-mode .volume-slider::-webkit-slider-thumb {
  background: #fff;
  border: 2px solid #2196F3;
}

.light-mode .volume-slider::-webkit-slider-thumb {
  background: #fff;
  border: 2px solid #2196F3;
}

.color-slider {
  width: 100%;
  height: 30px;
  padding: 0;
  margin: 0;
  border: none;
  border-radius: 5px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  cursor: pointer;
}

.color-slider::-webkit-color-swatch-wrapper {
  padding: 0;
}

.color-slider::-webkit-color-swatch {
  border: none;
  border-radius: 5px;
}

.color-slider::-moz-color-swatch {
  border: none;
  border-radius: 5px;
}

.rainbow {
  background: linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet);
  background-size: 400% 400%;
  animation: rainbow-animation 5s linear infinite;
}

.dark-mode .rainbow {
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.light-mode .rainbow {
  border: none;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
}

@keyframes rainbow-animation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@media (max-width: 768px) {
  h1 { font-size: 1.5rem; }
  h2 { font-size: 1.2rem; }
  .container { padding: 10px; }
  .music-box-list { flex-direction: column; gap: 10px; }
  .music-box { width: 100%; padding: 10px; }
  .settings-section { padding: 10px; }
}

@media (max-width: 480px) {
  h1 { font-size: 1.2rem; }
  h2 { font-size: 1rem; }
  .music-box-image { width: 80px; height: 80px; }
}
</style>