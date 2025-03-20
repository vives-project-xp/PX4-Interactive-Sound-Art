<template>
  <div class="container">
    <h1 class="title">Interactive Sound Art Controller</h1>
    <h2 class="subtitle">Select Your Music Box</h2>

    <div class="music-box-list">
      <div
        v-for="box in musicBoxes"
        :key="box.id"
        class="music-box"
        :class="{ 
          selected: selectedBox?.id === box.id, 
          pulsating: box.effect === 'pulsating' && box.isOn,
          firework: box.effect === 'firework' && box.isOn,
          rainbow: box.effect === 'rainbow' && box.isOn,
          off: !box.isOn 
        }"
        @click="selectBox(box)"
        :style="{
          boxShadow: box.isOn && box.effect !== 'rainbow' ? `0 0 20px ${box.color}` : 'none',
          backgroundColor: box.isOn && box.effect !== 'rainbow' ? box.color : 'transparent',
          '--box-color': box.color
        }"
      >
        <img :src="box.image" :alt="box.name" class="music-box-image" />
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
          <label>Effect:</label>
          <select v-model="selectedBox.effect" @change="updateEffect" class="effect-dropdown">
            <option value="pulsating">Pulsating</option>
            <option value="firework">Firework</option>
            <option value="rainbow">Rainbow</option>
          </select>
        </div>

        <div class="setting">
          <label>Sound:</label>
          <select v-model="selectedBox.sound" @change="updateSound(selectedBox)" class="sound-dropdown">
            <option v-for="sound in availableSounds" :key="sound" :value="sound">{{ sound }}</option>
          </select>
        </div>

        <div v-if="selectedBox.effect !== 'rainbow'" class="setting">
          <label>Color:</label>
          <input type="color" v-model="selectedBox.color" class="color-slider" @input="updateColor" />
        </div>

        <div class="setting">
          <label>LED State:</label>
          <input type="checkbox" v-model="selectedBox.led" @change="updateLED" />
        </div>
      </div>
    </div>

    <button v-if="selectedBox && selectedBox.color" @click="confirmSelection" class="confirm-button">
      Confirm Selection
    </button>
  </div>
</template>

<script>
import apiService from '../services/apiService.js';

export default {
  data() {
    return {
      musicBoxes: [],
      selectedBox: null,
      availableSounds: ['Piano', 'Guitar', 'Violin', 'Flute', 'Drums'],
      soundImages: {
        'Piano': '/image/piano.png',
        'Guitar': '/image/guitar.png',
        'Violin': '/image/violin.png',
        'Flute': '/image/flute.png',
        'Drums': '/image/drums.png',
      },
    };
  },

  async mounted() {
    try {
      this.musicBoxes = await apiService.getMusicBoxes();
    } catch {
      console.warn('Backend not available, using mock data');
      this.musicBoxes = [
        { id: 1, name: 'Box 1', image: this.soundImages['Piano'], color: '#ff0000', isOn: false, sound: 'Piano', effect: 'pulsating', led: false },
        { id: 2, name: 'Box 2', image: this.soundImages['Guitar'], color: '#00ff00', isOn: false, sound: 'Guitar', effect: 'firework', led: false },
        { id: 3, name: 'Box 3', image: this.soundImages['Violin'], color: '#0000ff', isOn: false, sound: 'Violin', effect: 'rainbow', led: false },
      ];
    }
  },

  methods: {
    selectBox(box) {
      this.selectedBox = box;
    },

    async togglePower(box) {
      box.isOn = !box.isOn;
      await apiService.togglePower(box.id, box.isOn);
    },

    async updateColor() {
      if (this.selectedBox) {
        await apiService.updateColor(this.selectedBox.id, this.selectedBox.color);
      }
    },

    async updateEffect() {
      if (this.selectedBox) {
        await apiService.updateEffect(this.selectedBox.id, this.selectedBox.effect);
      }
    },

    async updateLED() {
      if (this.selectedBox) {
        await apiService.updateLED(this.selectedBox.id, this.selectedBox.led);
      }
    },

    async updateSound(box) {
      box.image = this.soundImages[box.sound];
      await apiService.updateSound(box.id, box.sound);
    },

    confirmSelection() {
      alert(`You selected ${this.selectedBox.name} with color ${this.selectedBox.color}, effect ${this.selectedBox.effect}, sound ${this.selectedBox.sound}, and LED ${this.selectedBox.led ? 'On' : 'Off'}`);
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>

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
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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
  flex-wrap: wrap;
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
  width: 200px;
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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
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
  gap: 15px;
  align-items: center;
}

.setting {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.effect-dropdown, .sound-dropdown, .color-slider {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background: #0f0f0f;
  color: #fff;
  font-size: 1em;
}

.confirm-button {
  margin-top: 20px;
  padding: 10px 20px;
  border-radius: 5px;
  background: linear-gradient(97deg, #0096FF, #BB64FF 42%, #F2416B 74%, #EB7500);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1em;
}

.rainbow {
  background: linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet);
  background-size: 400% 400%;
  animation: rainbow-animation 5s linear infinite;
}

@keyframes rainbow-animation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.pulsating {
  animation: pulsate 1.5s infinite;
}

@keyframes pulsate {
  0% {
    box-shadow: 0 0 0 0 var(--box-color);
  }
  50% {
    box-shadow: 0 0 20px 10px var(--box-color);
  }
  100% {
    box-shadow: 0 0 0 0 var(--box-color);
  }
}

@media (max-width: 768px) {
  .music-box-list {
    flex-direction: column;
    align-items: center;
  }
}
</style>