import express from "express";
import http from "http";
import cors from "cors";
import { Server as SocketIOServer } from "socket.io";
import fetch from "node-fetch"; // Zorg dat je dit pakket hebt geïnstalleerd (npm install node-fetch)

const app = express();
const server = http.createServer(app);
const io = new SocketIOServer(server, {
  cors: { origin: "*" }
});
const PORT = 4000;

app.use(cors());
app.use(express.json());

// In-memory opslag voor devices en commando's
const devices = {}; // Bijvoorbeeld: { box1: { ip: "100.98.149.108", socketId: "abc123", lastSeen: 1680000000000 } }
const commands = {}; // Bijvoorbeeld: { box1: { instrument: "guitar", color: "#0000FF", effect: "rainbow", isOn: true } }

// HTTP-registratie endpoint voor apparaten
app.post("/register", (req, res) => {
  const { boxId, ip } = req.body;
  if (!boxId || !ip) {
    return res.status(400).json({ error: "boxId and ip are required" });
  }
  // Behoud eventueel een reeds bestaande socketId
  devices[boxId] = { ip, lastSeen: Date.now(), socketId: devices[boxId]?.socketId || null };
  console.log(`Device registered via HTTP: ${boxId} with IP ${ip}`);
  res.json({ message: "Registered successfully" });
});

// GET endpoint om alle devices met hun instellingen op te halen
app.get("/devices", (req, res) => {
  const combined = {};
  for (const boxId in devices) {
    combined[boxId] = {
      ...devices[boxId],
      settings: commands[boxId] || { instrument: "", color: "", effect: "", isOn: false }
    };
  }
  res.json(combined);
});

// Endpoint om commando's te ontvangen en door te sturen
app.post("/command/:boxId", (req, res) => {
  const { boxId } = req.params;
  const { instrument, color, effect, isOn } = req.body;
  commands[boxId] = { instrument, color, effect, isOn };
  console.log(`Command updated for ${boxId}:`, commands[boxId]);
  
  // Stuur het commando via WebSocket als het device is geregistreerd
  if (devices[boxId] && devices[boxId].socketId) {
    io.to(devices[boxId].socketId).emit("command", commands[boxId]);
    console.log(`Command sent via WebSocket to ${boxId}`);
  } else {
    console.error(`No WebSocket connection registered for ${boxId}`);
  }
  res.json({ message: "Command updated successfully", command: commands[boxId] });
});

// GET endpoint om de actuele status van een specifiek apparaat op te halen
app.get("/device/:boxId/status", async (req, res) => {
  const { boxId } = req.params;
  const device = devices[boxId];
  if (!device) {
    return res.status(404).json({ error: "Device not found" });
  }
  try {
    // Ga ervan uit dat de Pi zijn status beschikbaar stelt op poort 5000
    const response = await fetch(`http://${device.ip}:5000/status`);
    const status = await response.json();
    res.json(status);
  } catch (error) {
    res.status(500).json({ error: "Could not retrieve device status" });
  }
});

// Socket.IO verbindingen
io.on("connection", (socket) => {
  console.log("New socket connection:", socket.id);

  // Registratie via WebSocket
  socket.on("register", (data) => {
    const { boxId, ip } = data;
    if (boxId) {
      devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
      console.log(`Device registered via WebSocket: ${boxId} with IP ${ip}, socket: ${socket.id}`);
      socket.emit("register_ack", { message: "Registered via WebSocket successfully" });
    }
  });
  
  // Ontvang heartbeat berichten van de Pi
  socket.on("heartbeat", (data) => {
    const { boxId } = data;
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });
  
  // Verwijder apparaatregistratie bij disconnect
  socket.on("disconnect", () => {
    console.log("Socket disconnected:", socket.id);
    for (const boxId in devices) {
      if (devices[boxId].socketId === socket.id) {
        delete devices[boxId];
        console.log(`Device ${boxId} removed due to disconnection`);
      }
    }
  });
});

// Periodieke check om inactieve devices te verwijderen (bijv. na 60 sec geen heartbeat)
setInterval(() => {
  const now = Date.now();
  const threshold = 60000; // 60 seconden
  for (const boxId in devices) {
    if (now - devices[boxId].lastSeen > threshold) {
      console.log(`Device ${boxId} removed due to inactivity.`);
      delete devices[boxId];
    }
  }
}, 30000); // Check elke 30 seconden

server.listen(PORT, () => {
  console.log(`Backend server running on http://0.0.0.0:${PORT}`);
});
