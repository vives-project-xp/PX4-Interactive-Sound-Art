<script setup>
import { ref } from 'vue';

const musicBoxes = ref([
  { id: 1, name: 'Music Box 1' },
  { id: 2, name: 'Music Box 2' },
  { id: 3, name: 'Music Box 3' },
]);

const selectedMusicBox = ref(null);
const selectedColor = ref('#000000');

const selectMusicBox = (box) => {
  selectedMusicBox.value = box;
};

const selectColor = (event) => {
  selectedColor.value = event.target.value;
};
</script>

<template>
  <div class="start-screen">
    <h1>Select Your Music Box</h1>
    <div class="music-boxes">
      <div
        v-for="box in musicBoxes"
        :key="box.id"
        :class="['music-box', { selected: selectedMusicBox && selectedMusicBox.id === box.id }]"
        @click="selectMusicBox(box)"
      >
        {{ box.name }}
      </div>
    </div>
    <h2>Select Color</h2>
    <input type="color" v-model="selectedColor" @input="selectColor" />
    <div class="selected-info" v-if="selectedMusicBox">
      <h3>Selected Music Box: {{ selectedMusicBox.name }}</h3>
      <h3>Selected Color: <span :style="{ color: selectedColor }">{{ selectedColor }}</span></h3>
    </div>
  </div>
</template>

<style scoped>
.start-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.music-boxes {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.music-box {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.music-box.selected {
  background-color: #f0f0f0;
}

.selected-info {
  margin-top: 2rem;
  text-align: center;
}
</style>
