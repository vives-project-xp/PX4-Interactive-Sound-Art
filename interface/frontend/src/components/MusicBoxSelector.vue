<template>
  <div class="container">
    <h1 class="title">Interactive Sound Art Controller</h1>
    <h2 class="subtitle">Select Your Music Box</h2>

    <!-- Music Box Selection -->
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
        <!-- Music Box Image -->
        <img :src="box.image" :alt="box.name" class="music-box-image" />

        <!-- Box Name with Grey Background -->
        <p class="box-name">{{ box.name }}</p>

        <!-- On/Off Switch -->
        <div class="switch" @click.stop="togglePower(box)">
          <div :class="['slider', { on: box.isOn }]" />
        </div>
      </div>
    </div>

    <!-- Effect, Sound, and Color Selector -->
    <div v-if="selectedBox" class="settings-section">
      <h2>Settings for {{ selectedBox.name }}</h2>
      <div class="settings-grid">
        <!-- Effect Selector -->
        <div class="setting">
          <label>Effect:</label>
          <select v-model="selectedBox.effect" @change="updateEffect" class="effect-dropdown">
            <option value="pulsating">Pulsating</option>
            <option value="firework">Firework</option>
            <option value="rainbow">Rainbow</option>
          </select>
        </div>

        <!-- Sound Selector -->
        <div class="setting">
          <label>Sound:</label>
          <select v-model="selectedBox.sound" @change="updateSound(selectedBox)" class="sound-dropdown">
            <option v-for="sound in availableSounds" :key="sound" :value="sound">{{ sound }}</option>
          </select>
        </div>

        <!-- Color Picker (Hidden for Rainbow Effect) -->
        <div v-if="selectedBox.effect !== 'rainbow'" class="setting">
          <label>Color:</label>
          <input type="color" v-model="selectedBox.color" class="color-slider" @input="updateColor" />
        </div>
      </div>
    </div>

    <!-- Confirm Button -->
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
    };
  },

  async mounted() {
    this.musicBoxes = await apiService.getMusicBoxes();
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

    async updateSound(box) {
      await apiService.updateSound(box.id, box.sound);
    },

    confirmSelection() {
      alert(`You selected ${this.selectedBox.name} with color ${this.selectedBox.color}, effect ${this.selectedBox.effect}, and sound ${this.selectedBox.sound}`);
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: auto;
  text-align: center;
<<<<<<< HEAD
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(15px);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
=======
  background: 	#000;
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(15px);
  color: #fffffffb;
  display: flex;
  justify-content: flex-start;
  /* border: 2px solid #2998ff8d; */
  font-family: 'Orbitron', sans-serif; 
>>>>>>> d664b0913e5873b85206b61fe2b6fb988575e07c
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
<<<<<<< HEAD
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.5);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  width: 200px;
=======
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  width: 120px;
  border: 5px solid #ffffff70;
  transition: all 0.3s ease;
}

.music-box:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px #a972ff;
}

/* Selected Box */
.music-box.selected {
  transform: scale(1.1);
  box-shadow: 0 0 20px 5px #a972ff; /* Neon Glow when selected */
>>>>>>> d664b0913e5873b85206b61fe2b6fb988575e07c
}

.music-box-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.box-name {
  font-size: 1.2rem;
  font-weight: bold;
  background: rgba(0, 0, 0, 0.6); /* Grey-ish background for readability */
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
<<<<<<< HEAD
  border-radius: 5px;
  background: #0f0f0f;
=======
  border-radius: 10px;
  background-color: #0d2a46;
>>>>>>> d664b0913e5873b85206b61fe2b6fb988575e07c
  color: #fff;
  font-size: 1em;
  border: 5px
}

.confirm-button {
  margin-top: 20px;
<<<<<<< HEAD
  padding: 10px 20px;
  border-radius: 5px;
  background: linear-gradient(97deg, #0096FF, #BB64FF 42%, #F2416B 74%, #EB7500);
=======
  padding: 12px 20px;
  border: none;
  background: #0d2a46;
>>>>>>> d664b0913e5873b85206b61fe2b6fb988575e07c
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1em;
}

/* Rainbow Effect */
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

/* Pulsating Effect */
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

<<<<<<< HEAD
@media (max-width: 768px) {
  .music-box-list {
    flex-direction: column;
    align-items: center;
  }
=======
button:hover {
  background: #a872ffcf;;
>>>>>>> d664b0913e5873b85206b61fe2b6fb988575e07c
}
</style>