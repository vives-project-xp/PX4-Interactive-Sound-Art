// backend/index.js
import express from "express";
import cors from "cors";
import axios from "axios";

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

// In-memory storage for commands per box
const commands = {};

// GET endpoint: Retrieve current command for a box
app.get("/command/:boxId", (req, res) => {
  const { boxId } = req.params;
  res.json(commands[boxId] || { instrument: "", color: "", effect: "" });
});

// POST endpoint: Update command for a box and forward it to the Raspberry Pi
app.post("/command/:boxId", async (req, res) => {
  const { boxId } = req.params;
  const { instrument, color, effect } = req.body;

  commands[boxId] = { instrument, color, effect };
  console.log(`✅ Command updated for ${boxId}:`, commands[boxId]);

  // Replace with your actual Raspberry Pi IP and port (see below)
  const raspberryPiURL = "http://192.168.1.100:5000"; 
  try {
    await axios.post(`${raspberryPiURL}/update`, commands[boxId]);
    console.log(`✅ Command sent to Raspberry Pi:`, commands[boxId]);
  } catch (error) {
    console.error("❌ Failed to send command to Raspberry Pi:", error.message);
  }

  res.json({ message: "Command updated successfully", command: commands[boxId] });
});

// Start the server
app.listen(PORT, "0.0.0.0", () => {
  console.log(`🚀 Backend server running on http://0.0.0.0:${PORT}`);
});
