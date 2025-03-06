<template>
  <div class="container">
    <h1>Select Your Music Box</h1>

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
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  color: #fff;
}

/* Music Box List */
.music-box-list {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

/* Music Box */
.music-box {
  padding: 15px;
  border-radius: 10px;
  transition: 0.3s;
  cursor: pointer;
  text-align: center;
  width: 120px;
  height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  background: white;
  position: relative;
}

/* Selected Box */
.music-box.selected {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3);
}

/* Greyed Out Effect */
.music-box.off {
  filter: grayscale(100%);
  opacity: 0.5;
  pointer-events: auto;
}

/* Pulsing Effect */
.pulsing {
  animation: heartbeat 0.5s infinite ease-in-out;
}

@keyframes heartbeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Music Box Image */
.music-box-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

/* Color Display Box */
.color-display {
  width: 60px;
  height: 60px;
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
  padding: 10px 20px;
  border: none;
  background: #ff0077;
  color: white;
  cursor: pointer;
  border-radius: 10px;
  font-weight: bold;
  transition: 0.3s;
}

button:hover {
  background: #cc0055;
}
</style>
