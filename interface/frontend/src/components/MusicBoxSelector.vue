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
          solid: box.effect === 'solid' && box.isOn,
          puls: box.effect === 'puls' && box.isOn,
          chase: box.effect === 'chase' && box.isOn,
          rainbow: box.effect === 'rainbow' && box.isOn,
          fire: box.effect === 'fire' && box.isOn,
          sparkle: box.effect === 'sparkle' && box.isOn,
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
            <option value="solid">Solid</option>
            <option value="puls">Puls</option>
            <option value="chase">Chase</option>
            <option value="fire">Fire</option>
            <option value="sparkle">Sparkle</option>
            <option value="firework">Firework</option>
            <option value="rainbow">Rainbow</option>
          </select>
        </div>

        <div class="setting">
          <label>Instrument:</label>
          <select v-model="selectedBox.sound" @change="updateSound(selectedBox)" class="sound-dropdown">
            <option v-for="sound in availableSounds" :key="sound" :value="sound">{{ sound }}</option>
          </select>
        </div>

        <div v-if="selectedBox.effect !== 'rainbow'" class="setting">
          <label>Color:</label>
          <input type="color" v-model="selectedBox.color" class="color-slider" @input="updateColor" />
        </div>
      </div>
    </div>

    
  </div>
</template>

<script>
import apiService from '../services/apiService.js';

export default {
  data() {
    return {
      musicBoxes: [],
      selectedBox: null,
      availableSounds: ['gitaar', 'drum', 'bass jumpy', 'bell', 'synth Sci-Fi','synth sharp', 'bassline'],
      soundImages: {
        'gitaar': '/image/gitaar.png',
        'drum': '/image/drum.png',
        'bass jumpy': '/image/bassjumpy.png',
        'bell': '/image/bel.png',
        'synth Sci-Fi': '/image/synthscifi.png',
        'synth sharp': '/image/synthsharp.png',
        'bassline': '/image/bassline.png',
        
      },
    };
  },

  async mounted() {
    // Get initial devices
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

    // Listen for real-time updates from the backend
    this.$socket.on('command', (data) => {
      console.log('Received command via WebSocket:', data);
      const index = this.musicBoxes.findIndex(box => box.id === data.boxId);
      if (index !== -1) {
        this.musicBoxes[index] = {
          ...this.musicBoxes[index],
          ...data,
        };
      }
    });

    this.$socket.on('update-settings', (data) => {
      console.log('Received settings update via WebSocket:', data);
      const index = this.musicBoxes.findIndex(box => box.id === data.boxId);
      if (index !== -1) {
        this.musicBoxes[index] = {
          ...this.musicBoxes[index],
          ...data.settings,
        };
      }
    });
  },

  methods: {
    selectBox(box) {
      this.selectedBox = box;
    },

    async togglePower(box) {
      box.isOn = !box.isOn;
      await apiService.togglePower(box.id, box.isOn);
      this.$socket.emit('update-settings', { boxId: box.id, settings: { isOn: box.isOn } });
    },

    async updateColor() {
      if (this.selectedBox) {
        await apiService.updateColor(this.selectedBox.id, this.selectedBox.color);
        this.$socket.emit('update-settings', { boxId: this.selectedBox.id, settings: { color: this.selectedBox.color } });
      }
    },

    async updateEffect() {
      if (this.selectedBox) {
        await apiService.updateEffect(this.selectedBox.id, this.selectedBox.effect);
        this.$socket.emit('update-settings', { boxId: this.selectedBox.id, settings: { effect: this.selectedBox.effect } });
      }
    },

    async updateSound(box) {
      box.image = this.soundImages[box.sound];
      await apiService.updateSound(box.id, box.sound);
      this.$socket.emit('update-settings', { boxId: box.id, settings: { sound: box.sound, image: box.image } });
    },

    async confirmSelection() {
      // Also update the instrument (sound) selection when confirming.
      await apiService.updateSound(this.selectedBox.id, this.selectedBox.sound);
      alert(`You selected ${this.selectedBox.name} with color ${this.selectedBox.color}, effect ${this.selectedBox.effect}, instrument ${this.selectedBox.sound}, and LED ${this.selectedBox.led ? 'On' : 'Off'}`);
      this.$socket.emit('update-settings', {
        boxId: this.selectedBox.id,
        settings: {
          color: this.selectedBox.color,
          effect: this.selectedBox.effect,
          sound: this.selectedBox.sound,
          led: this.selectedBox.led,
        },
      });
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
  h1 {
    font-size: 1.5rem;
  }
  h2 {
    font-size: 1.2rem;
  }
  .container {
    padding: 10px;
  }
  .music-box-list {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
  .music-box {
    width: 100%;
    padding: 10px;
  }
  .settings-section {
    padding: 10px;
  }
  
  .box-name {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.2rem;
  }
  h2 {
    font-size: 1rem;
  }
  .music-box-image {
    width: 80px;
    height: 80px;
  }
}
</style>
