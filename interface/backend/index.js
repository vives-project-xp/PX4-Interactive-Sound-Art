import express from "express";
import cors from "cors";
import axios from "axios";

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

// In-memory opslag voor geregistreerde apparaten (boxes) en commando's
const devices = {};  // Bijvoorbeeld: { box1: { ip: "10.10.2.48", lastSeen: 1680000000000 } }
const commands = {};

// GET endpoint: Haal alle geregistreerde apparaten (Raspberry Pi's) op
app.get("/devices", (req, res) => {
  res.json(devices);
});

// Registratie-endpoint voor een Raspberry Pi-box
app.post("/register", (req, res) => {
  const { boxId, ip } = req.body;
  if (!boxId || !ip) {
    return res.status(400).json({ error: "boxId and ip are required" });
  }
  devices[boxId] = { ip, lastSeen: Date.now() };
  console.log(`Device registered: ${boxId} with IP ${ip}`);
  res.json({ message: "Registered successfully" });
});

// GET endpoint: Haal het huidige commando op voor een box
app.get("/command/:boxId", (req, res) => {
  const { boxId } = req.params;
  res.json(commands[boxId] || { instrument: "", color: "", effect: "" });
});

// POST endpoint: Update het commando voor een box en stuur dit door naar de Raspberry Pi
app.post("/command/:boxId", async (req, res) => {
  const { boxId } = req.params;
  const { instrument, color, effect } = req.body;
  
  // Sla het commando lokaal op
  commands[boxId] = { instrument, color, effect };
  console.log(`Command updated for ${boxId}:`, commands[boxId]);
  
  // Kijk of de box (Raspberry Pi) geregistreerd is
  const device = devices[boxId];
  if (device) {
    const raspberryPiURL = `http://${device.ip}:5000`; // De Pi draait op poort 5000
    try {
      await axios.post(`${raspberryPiURL}/update`, commands[boxId]);
      console.log(`Command sent to Raspberry Pi:`, commands[boxId]);
    } catch (error) {
      console.error("Failed to send command to Raspberry Pi:", error.message);
    }
  } else {
    console.error(`No registered device for box ${boxId}`);
  }
  
  res.json({ message: "Command updated successfully", command: commands[boxId] });
});

// Start de backend-server
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Backend server running on http://0.0.0.0:${PORT}`);
});
