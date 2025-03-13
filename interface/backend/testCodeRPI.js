// rpi_server.js
import express from "express";
import cors from "cors";
import ws281x from "rpi-ws281x-native";

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

const NUM_LEDS = 60; // Change to match your LED strip length
const pixelData = new Uint32Array(NUM_LEDS);
ws281x.init(NUM_LEDS);

// Function to update the LED strip based on color and effect
function updateLEDs(color, effect) {
  // Convert hex string (e.g. "#ff0000") to integer (assumes no alpha channel)
  const hex = color.startsWith("#") ? color.slice(1) : color;
  const intColor = parseInt(hex, 16);

  if (effect === "solid") {
    // Solid color: fill all LEDs
    for (let i = 0; i < NUM_LEDS; i++) {
      pixelData[i] = intColor;
    }
    ws281x.render(pixelData);
  } else if (effect === "strobe") {
    // Strobe effect: flash on/off repeatedly
    let on = true;
    let iterations = 10;
    const interval = setInterval(() => {
      for (let i = 0; i < NUM_LEDS; i++) {
        pixelData[i] = on ? intColor : 0;
      }
      ws281x.render(pixelData);
      on = !on;
      iterations--;
      if (iterations <= 0) {
        clearInterval(interval);
      }
    }, 100);
  } else if (effect === "fire") {
    // Fire effect: alternate full brightness and half brightness on LEDs
    for (let i = 0; i < NUM_LEDS; i++) {
      if (i % 2 === 0) {
        pixelData[i] = intColor;
      } else {
        const r = (((intColor >> 16) & 0xff) >> 1);
        const g = (((intColor >> 8) & 0xff) >> 1);
        const b = ((intColor & 0xff) >> 1);
        pixelData[i] = (r << 16) | (g << 8) | b;
      }
    }
    ws281x.render(pixelData);
  } else {
    // Default to solid
