import express from "express";
import http from "http";
import cors from "cors";
import { Server as SocketIOServer } from "socket.io";

const app = express();
const server = http.createServer(app);
const io = new SocketIOServer(server, { cors: { origin: "*" } });
const PORT = 4000;

app.use(cors());
app.use(express.json());

// In-memory opslag
const devices = {};
const commands = {};

// Socket.IO events
io.on("connection", (socket) => {
  console.log("Nieuwe socket-verbinding:", socket.id);

  // Device of frontend registratie
  socket.on("register", ({ boxId, ip, client }) => {
    console.log(`Geregistreerd via WebSocket door ${client || 'onbekend'} (socket: ${socket.id})`);
    if (boxId) {
      devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
      console.log(`Geregistreerd via WebSocket: ${boxId} (${client || 'device'})`);
      socket.emit("register_ack", { success: true });
    }
  });
  

  // Update settings van frontend
  socket.on("update-settings", ({ boxId, settings }) => {
    // Werk commandes bij
    commands[boxId] = { ...commands[boxId], ...settings };
    const payload = { boxId, ...commands[boxId] };

    // Stuur naar specifiek device
    const device = devices[boxId];
    if (device?.socketId) {
      io.to(device.socketId).emit("command", payload);
      console.log(`Verzonden naar device ${boxId}:`, payload);
    }

    // Broadcast naar andere UIs
    socket.broadcast.emit("command", payload);
    console.log(`Gebroadcast naar andere clients:`, payload);
  });

  // Heartbeat van devices
  socket.on("heartbeat", ({ boxId }) => {
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });

  socket.on("disconnect", () => {
    console.log("Socket disconnected:", socket.id);
    // Cleanup inactieve registraties
    for (const boxId in devices) {
      if (devices[boxId].socketId === socket.id) {
        delete devices[boxId];
        console.log(`Verwijderd door disconnect: ${boxId}`);
      }
    }
  });
});

// Periodieke check voor inactiviteit
setInterval(() => {
  const now = Date.now();
  for (const boxId in devices) {
    if (now - devices[boxId].lastSeen > 60000) {
      delete devices[boxId];
      console.log(`Verwijderd wegens inactiviteit: ${boxId}`);
    }
  }
}, 30000);

server.listen(PORT, () => {
  console.log(`Backend draait op http://0.0.0.0:${PORT}`);
});