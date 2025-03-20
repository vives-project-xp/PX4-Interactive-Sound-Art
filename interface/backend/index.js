import express from "express";
import http from "http";
import cors from "cors";
import { Server as SocketIOServer } from "socket.io";

const app = express();
const server = http.createServer(app);
const io = new SocketIOServer(server, {
  cors: { origin: "*" }
});
const PORT = 4000;

app.use(cors());
app.use(express.json());

// In-memory storage for devices and commands
const devices = {}; // e.g., { box1: { ip: "100.98.149.108", socketId: "abc123", lastSeen: 1680000000000 } }
const commands = {}; // e.g., { box1: { instrument: "guitar", color: "#0000FF", effect: "rainbow", isOn: true } }

// HTTP registration endpoint for devices
app.post("/register", (req, res) => {
  const { boxId, ip } = req.body;
  if (!boxId || !ip) {
    return res.status(400).json({ error: "boxId and ip are required" });
  }
  devices[boxId] = { ip, lastSeen: Date.now() };
  console.log(`Device registered via HTTP: ${boxId} with IP ${ip}`);
  res.json({ message: "Registered successfully" });
});

// GET endpoint to fetch devices with their settings
app.get("/devices", (req, res) => {
  // Combine device data with command settings
  const combined = {};
  for (const boxId in devices) {
    combined[boxId] = {
      ...devices[boxId],
      settings: commands[boxId] || { instrument: "", color: "", effect: "", isOn: false }
    };
  }
  res.json(combined);
});

// Endpoint to receive commands from the frontend
app.post("/command/:boxId", (req, res) => {
  const { boxId } = req.params;
  const { instrument, color, effect, isOn } = req.body;
  commands[boxId] = { instrument, color, effect, isOn };
  console.log(`Command updated for ${boxId}:`, commands[boxId]);

  // If a device is connected via WebSocket, send the command
  if (devices[boxId] && devices[boxId].socketId) {
    io.to(devices[boxId].socketId).emit("command", commands[boxId]);
    console.log(`Command sent via WebSocket to ${boxId}`);
  } else {
    console.error(`No WebSocket connection registered for ${boxId}`);
  }
  res.json({ message: "Command updated successfully", command: commands[boxId] });
});

// Socket.IO connection handling
io.on("connection", (socket) => {
  console.log("New socket connection:", socket.id);

  // Device registers via a "register" event with boxId
  socket.on("register", (data) => {
    const { boxId, ip } = data;
    if (boxId) {
      devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
      console.log(`Device registered via WebSocket: ${boxId} with IP ${ip}, socket: ${socket.id}`);
      socket.emit("register_ack", { message: "Registered via WebSocket successfully" });
    }
  });

  // Remove device registration on disconnect
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

server.listen(PORT, () => {
  console.log(`Backend WebSocket server running on http://0.0.0.0:${PORT}`);
});
