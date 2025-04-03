import express from "express";
import http from "http";
import cors from "cors";
import { Server as SocketIOServer } from "socket.io";
import fetch from "node-fetch"; // Zorg dat dit pakket geïnstalleerd is

const app = express();
const server = http.createServer(app);
const io = new SocketIOServer(server, { cors: { origin: "*" } });
const PORT = 4000;

app.use(cors());
app.use(express.json());

// In-memory opslag voor devices en commando's
const devices = {};
const commands = {};

// HTTP endpoint voor registratie van apparaten
app.post("/register", (req, res) => {
  const { boxId, ip } = req.body;
  if (!boxId || !ip) {
    return res.status(400).json({ error: "boxId and ip are required" });
  }
  devices[boxId] = { ip, lastSeen: Date.now(), socketId: devices[boxId]?.socketId || null };
  console.log(`Device geregistreerd via HTTP: ${boxId} met IP ${ip}`);
  res.json({ message: "Registered successfully" });
});

// Endpoint om alle devices met hun instellingen op te halen
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

// Endpoint om commando's te ontvangen en te verspreiden
app.post("/command/:boxId", (req, res) => {
  const { boxId } = req.params;
  const { instrument, color, effect, isOn } = req.body;
  commands[boxId] = { instrument, color, effect, isOn };
  console.log(`Command geüpdatet voor ${boxId}:`, commands[boxId]);
  
  // Verstuur het commando via WebSocket indien de client geregistreerd is
  if (devices[boxId] && devices[boxId].socketId) {
    io.to(devices[boxId].socketId).emit("command", commands[boxId]);
    console.log(`Command verzonden via WebSocket naar ${boxId}`);
  } else {
    console.error(`Geen WebSocket-verbinding voor ${boxId}`);
  }
  res.json({ message: "Command succesvol geüpdatet", command: commands[boxId] });
});

// Endpoint om de status van een specifiek apparaat op te halen
app.get("/device/:boxId/status", async (req, res) => {
  const { boxId } = req.params;
  const device = devices[boxId];
  if (!device) {
    return res.status(404).json({ error: "Device not found" });
  }
  try {
    const response = await fetch(`http://${device.ip}:5000/status`);
    const status = await response.json();
    res.json(status);
  } catch (error) {
    res.status(500).json({ error: "Kon status van apparaat niet ophalen" });
  }
});

// Socket.IO verbindingen
io.on("connection", (socket) => {
  console.log("Nieuwe socket-verbinding:", socket.id);

  // Registratie via WebSocket
  socket.on("register", (data) => {
    const { boxId, ip } = data;
    if (boxId) {
      devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
      console.log(`Device geregistreerd via WebSocket: ${boxId} met IP ${ip}, socket: ${socket.id}`);
      socket.emit("register_ack", { message: "Registered via WebSocket successfully" });
    }
  });
  
  // Ontvang heartbeat berichten
  socket.on("heartbeat", (data) => {
    const { boxId } = data;
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });
  
  // Verwijder device registratie bij disconnect
  socket.on("disconnect", () => {
    console.log("Socket disconnected:", socket.id);
    for (const boxId in devices) {
      if (devices[boxId].socketId === socket.id) {
        delete devices[boxId];
        console.log(`Device ${boxId} verwijderd door disconnect`);
      }
    }
  });
});

// Periodieke check voor inactieve devices
setInterval(() => {
  const now = Date.now();
  const threshold = 60000;
  for (const boxId in devices) {
    if (now - devices[boxId].lastSeen > threshold) {
      console.log(`Device ${boxId} verwijderd wegens inactiviteit.`);
      delete devices[boxId];
    }
  }
}, 30000);

server.listen(PORT, () => {
  console.log(`Backend server draait op http://0.0.0.0:${PORT}`);
});
