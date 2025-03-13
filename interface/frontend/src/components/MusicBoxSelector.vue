<template>
  <div class="container">
    <h1>Interactive Sound Art Controller</h1>
    <h2>Select Your Music Box</h2>

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
          boxShadow: box.isOn ? `0 0 20px ${box.color}` : 'none',
          backgroundColor: box.isOn ? box.color : 'transparent',
          '--box-color': box.color
        }"
      >
        <!-- Music Box Image -->
        <img :src="box.image" :alt="box.name" class="music-box-image" />

        <!-- Color Display Box -->
        <div class="color-display" :style="{ backgroundColor: box.color, opacity: box.isOn ? 1 : 0.3 }"></div>

        <p>{{ box.name }}</p>

        <!-- On/Off Switch -->
        <div class="switch" @click.stop="togglePower(box)">
          <div :class="['slider', { on: box.isOn }]"></div>
        </div>
      </div>
    </div>

    

    <!-- Effect Selector -->
<div v-if="selectedBox" class="effect-selector">
  <h2>Select Effect</h2>
  <select v-model="selectedBox.effect" @change="updateEffect" class="effect-dropdown">
    <option value="pulsating">Pulsating</option>
    <option value="firework">Firework</option>
    <option value="rainbow">Rainbow</option>
  </select>
</div>

<!-- Color Picker Section (Hidden if Rainbow is Selected) -->
<div v-if="selectedBox && selectedBox.effect !== 'rainbow'" class="color-picker">
  <h2>Choose a Color</h2>
  <input type="color" v-model="selectedBox.color" class="color-slider" @input="updateColor" />
</div>


    <!-- Confirm Button -->
    <button v-if="selectedBox && selectedBox.color" @click="confirmSelection">
      Confirm Selection
    </button>
  </div>
</template>

<script>
import apiService from '../services/apiService.js';  // Importing the API service

export default {
  data() {
    return {
      musicBoxes: [],  // To hold the fetched music boxes
      selectedBox: null,  // To hold the currently selected music box
    };
  },

  async mounted() {
    // Fetch music boxes from the backend (or mock data if backend is unavailable)
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

    confirmSelection() {
      alert(`You selected ${this.selectedBox.name} with color ${this.selectedBox.color} and effect ${this.selectedBox.effect}`);
    },
  },
};
</script>

<style scoped>
/* Container Styling */
.container {
  flex-direction: column;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  background: 	#000;
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(15px);
  color: #2997ff;;
  display: flex;
  justify-content: flex-start;
  border: 2px solid #2998ff8d;
  font-family: 'Orbitron', sans-serif; 
}

/* h1, h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #0ff;
  text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 30px #0ff;
} */

h1, h2 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(97deg, #0096FF, #BB64FF 42%, #F2416B 74%, #EB7500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: none; /* Verwijder de oude text-shadow om het effect beter te laten werken */
}


/* Music Box List */
.music-box-list {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin: 20px 0;
}

/* Music Box */
.music-box {
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  width: 150px;
  border: 1px solid #a972ff;
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
}

/* Greyed Out Effect */
.music-box.off {
  filter: grayscale(100%);
  opacity: 0.5;
  pointer-events: auto;
}

/* Pulsating Glow Effect */
.pulsating {
  animation: pulsateGlow 1s infinite ease-in-out;
}

@keyframes pulsateGlow {
  0% { box-shadow: 0 0 15px var(--box-color); }
  50% { box-shadow: 0 0 75px var(--box-color); }
  100% { box-shadow: 0 0 15px var(--box-color); }
}

/* Firework Effect */
.firework {
  animation: fireworkEffect 1s infinite;
}

@keyframes fireworkEffect {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; box-shadow: 0 0 10px rgba(255, 255, 255, 0.5), 0 0 20px rgba(255, 255, 255, 0.3); }
  100% { transform: scale(1); opacity: 1; }
}

/* Rainbow Effect */
.rainbow {
  animation: rainbowGlow 1s infinite linear;
}

@keyframes rainbowGlow {
  0% { box-shadow: 0 0 10px red, 0 0 20px orange, 0 0 30px yellow, 0 0 40px green, 0 0 50px cyan, 0 0 60px blue, 0 0 70px violet; }
  100% { box-shadow: 0 0 10px violet, 0 0 20px blue, 0 0 30px cyan, 0 0 40px green, 0 0 50px yellow, 0 0 60px orange, 0 0 70px red; }
}

/* Music Box Image */
.music-box-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  transition: transform 0.3s;
}

/* Color Display Box */
.color-display {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  margin-top: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  transition: background 0.3s;
}

/* Power Switch */
.switch {
  width: 40px;
  height: 20px;
  background: #ccc;
  border-radius: 20px;
  display: flex;
  align-items: center;
  padding: 2px;
  cursor: pointer;
  transition: 0.3s;
}

.slider {
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
  transform: translateX(0);
}

.on {
  transform: translateX(20px);
  background: limegreen;
}

/* Effect Selector */
.effect-selector {
  margin-top: 20px;
}

.effect-dropdown {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  background-color: #2998ff42;
  color: #fff;
  font-size: 1em;
  border: 5px
}

/* Confirm Button */
button {
  margin-top: 20px;
  padding: 12px 20px;
  border: none;
  background: #2998ff42;
  color: white;
  cursor: pointer;
  border-radius: 10px;
  font-weight: bold;
  transition: 0.3s;
  font-size: 1.2em;
}

button:hover {
  background: #a872ffcf;;
}
</style>
