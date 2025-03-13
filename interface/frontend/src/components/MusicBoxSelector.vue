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
          pulsing: box.isOn && selectedBox?.id === box.id && selectedBox.color,
          off: !box.isOn 
        }"
        @click="selectBox(box)"
        :style="{ boxShadow: box.isOn ? `0 0 20px ${box.color}` : 'none' }"
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

    <!-- Color Picker Section -->
    <div v-if="selectedBox" class="color-picker">
      <h2>Choose a Color</h2>
      <input type="color" v-model="selectedBox.color" class="color-slider" />
    </div>

    <!-- Confirm Button -->
    <button v-if="selectedBox && selectedBox.color" @click="confirmSelection">
      Confirm Selection
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      musicBoxes: [
        { id: 1, name: "Classic Box", image: "/image/box.png", color: "#ff0000", isOn: false },
        { id: 2, name: "Modern Box", image: "/image/box.png", color: "#00ff00", isOn: false },
        { id: 3, name: "Retro Box", image: "/image/box.png", color: "#0000ff", isOn: false },
      ],
      selectedBox: null,
    };
  },
    
  methods: {
    selectBox(box) {
      this.selectedBox = box;
    },
    togglePower(box) {
      box.isOn = !box.isOn;
    },
    confirmSelection() {
      alert(`You selected ${this.selectedBox.name} with color ${this.selectedBox.color}`);
    },
  },
};
</script>

<style scoped>
/* Container Styling */
.container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  background: rgba(0, 0, 0, 0.8);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(15px);
  color: #0ff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.5);
  font-family: 'Orbitron', sans-serif; 
}


h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #0ff;
  text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 30px #0ff;
  width: 100%;
  text-align: center;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #0ff;
  text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 30px #0ff;
  width: 100%;
  text-align: center; 
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
  transition: 0.3s;
  cursor: pointer;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  width: 150px;
  border: 1px solid rgba(0, 255, 255, 0.5);
}

.music-box:hover {
  transform: scale(1.05);
}

/* Selected Box */
.music-box.selected {
  transform: scale(1.1);
}

/* Greyed Out Effect */
.music-box.off {
  filter: grayscale(100%);
  opacity: 0.5;
  pointer-events: auto;
}

/* Pulsing Effect */
.pulsing {
  animation: heartbeat 1s infinite ease-in-out;
}

@keyframes heartbeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
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

/* Color Picker */
.color-picker {
  margin-top: 20px;
}

.color-slider {
  width: 100%;
  height: 40px;
  border: none;
  cursor: pointer;
  background: none;
}

/* Confirm Button */
button {
  margin-top: 20px;
  padding: 12px 20px;
  border: none;
  background: #ff0077;
  color: white;
  cursor: pointer;
  border-radius: 10px;
  font-weight: bold;
  transition: 0.3s;
  font-size: 1.2em;
  box-shadow: 0 0 10px #ff0077, 0 0 20px #ff0077, 0 0 30px #ff0077;
}

button:hover {
  background: #cc0055;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  h1 {
    font-size: 1.5em;
  }

  h2 {
    font-size: 1.2em;
  }

  .music-box-list {
    flex-direction: column;
    align-items: center;
  }

  .music-box {
    width: 100%;
    height: auto;
  }

  .music-box-image {
    width: 60px;
    height: 60px;
  }

  button {
    width: 100%;
    font-size: 1em;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.2em;
  }

  h2 {
    font-size: 1em;
  }

  .container {
    padding: 10px;
  }

  .music-box {
    width: 100px;
    height: 150px;
  }

  .music-box-image {
    width: 50px;
    height: 50px;
  }

  button {
    padding: 12px 0;
    font-size: 14px;
  }
}
</style>