<template>
    <div class="settings">
      <h2>Configureer Box: {{ boxId }}</h2>
      <label>
        Instrument:
        <input v-model="command.instrument" type="text" />
      </label>
      <label>
        Kleur:
        <input v-model="command.color" type="color" />
      </label>
      <label>
        Effect:
        <input v-model="command.effect" type="text" />
      </label>
      <button @click="saveCommand">Opslaan</button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { fetchCommand, updateCommand } from "../api";  // Let op: "../api" omdat api.js in src/ staat
  
  // Ontvang de boxId als prop (indien nodig)
  const props = defineProps({
    boxId: {
      type: String,
      default: "box1",
    },
  });
  
  const command = ref({ instrument: "", color: "", effect: "" });
  
  async function loadCommand() {
    command.value = await fetchCommand(props.boxId);
  }
  
  async function saveCommand() {
    await updateCommand(props.boxId, command.value);
    alert("Command updated!");
  }
  
  onMounted(loadCommand);
  </script>
  
  <style scoped>
  .settings {
    margin: 20px;
  }
  label {
    display: block;
    margin: 10px 0;
  }
  </style>
  