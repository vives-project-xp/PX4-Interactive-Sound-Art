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

// In-memory opslag voor apparaten en sockets
const devices = {}; // Bijvoorbeeld: { box1: { ip: "100.98.149.108", socketId: "abc123", lastSeen: 1680000000000 } }
const commands = {};

// Registratie via HTTP (optioneel) om apparaten ook te kunnen registreren via POST
app.post("/register", (req, res) => {
  const { boxId, ip } = req.body;
  if (!boxId || !ip) {
    return res.status(400).json({ error: "boxId and ip are required" });
  }
  devices[boxId] = { ip, lastSeen: Date.now() };
  console.log(`Device registered via HTTP: ${boxId} with IP ${ip}`);
  res.json({ message: "Registered successfully" });
});

// Endpoint om een commando te ontvangen (van bijvoorbeeld een Vue frontend)
app.post("/command/:boxId", (req, res) => {
  const { boxId } = req.params;
  const { instrument, color, effect } = req.body;
  commands[boxId] = { instrument, color, effect };
  console.log(`Command updated for ${boxId}:`, commands[boxId]);
  
  // Als er een socket verbonden is voor deze box, stuur het commando via websockets
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
  console.log("New socket connection: ", socket.id);
  
  // Het apparaat registreert zich via een "register" event met de boxId
  socket.on("register", (data) => {
    const { boxId, ip } = data;
    if (boxId) {
      devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
      console.log(`Device registered via WebSocket: ${boxId} with IP ${ip}, socket: ${socket.id}`);
      socket.emit("register_ack", { message: "Registered via WebSocket successfully" });
    }
  });
  
  // Als een socket disconnect, verwijder dan de registratie
  socket.on("disconnect", () => {
    console.log("Socket disconnected: ", socket.id);
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
