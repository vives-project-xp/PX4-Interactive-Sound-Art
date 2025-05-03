<template>
  <div class="container">
    <h1 class="title">Interactive Sound Art Controller</h1>

    <div class="music-box-list">
      <div
        v-for="box in musicBoxes"
        :key="box.id"
        class="music-box"
        :class="{ selected: selectedBox && selectedBox.id === box.id, off: !box.isOn }"
        @click="selectBox(box)"
        :style="{
          boxShadow: box.isOn ? `0 0 20px ${box.color}` : 'none',
          backgroundColor: box.isOn ? box.color : 'transparent'
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
    };
  },
  mounted() {
    // register this UI
    socketService.emit("register", { client: "frontend" });

    // receive initial list of already-connected boxes
    socketService.on("devices-list", (list) => {
      this.musicBoxes = list.map(({ boxId, ip }) => ({
        id: boxId,
        ip,
        name: `Box ${boxId}`,
        isOn: false,
        color: "#FF0000",
        effect: "solid",
        instrument: "gitaar",
      }));
    });

    // handle updates from any client or Pi
    socketService.on("command", (data) => {
      console.log("⚡️ [Vue] received command:", data);
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
          image: "/placeholder.png",
          isOn: false,
          color: "#ff0000",
          effect: "solid",
          instrument: "Gitaar",
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
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: auto;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(15px);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
}

h1, h2 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(97deg, #0096FF, #BB64FF 42%, #F2416B 74%, #EB7500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.5);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.music-box.selected {
  transform: scale(1.05);
}

.music-box.off {
  opacity: 0.4;
}

.music-box-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.box-name {
  font-size: 1.2rem;
  font-weight: bold;
  background: rgba(0, 0, 0, 0.6);
  padding: 5px 10px;
  border-radius: 5px;
  margin: 10px 0;
  color: white;
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

.settings-section {
  margin-top: 20px;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid rgba(0, 255, 255, 0.5);
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

.color-slider {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.color-slider::-webkit-color-swatch {
  border-radius: 3px;
  border: none;
}

.color-slider::-moz-color-swatch {
  border: none;
}

.effect-dropdown,
.sound-dropdown {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  background: #0f0f0f;
  color: #fff;
  font-size: 1em;
  border: none;
}

.color-slider {
  width: 100%;
  padding: 3px;
  border-radius: 5px;
  background: #0f0f0f;
  color: #fff;
  font-size: 1em;
  border: none;
}

.rainbow {
  background: linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet);
  background-size: 400% 400%;
  animation: rainbow-animation 5s linear infinite;
}

@keyframes rainbow-animation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.pulsating {
  animation: pulsate 1.5s infinite;
}

@keyframes pulsate {
  0% { box-shadow: 0 0 0 0 var(--box-color); }
  50% { box-shadow: 0 0 20px 10px var(--box-color); }
  100% { box-shadow: 0 0 0 0 var(--box-color); }
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
