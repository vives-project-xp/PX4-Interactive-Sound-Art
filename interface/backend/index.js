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

// In-memory opslag van devices en hun laatste status
const devices = {};
const commands = {};

// Socket.IO events
io.on("connection", (socket) => {
  console.log("Nieuwe socket-verbinding:", socket.id);

  // Register (frontend of RPi)
  socket.on("register", ({ boxId, ip, client }) => {
    if (!boxId) return;
    devices[boxId] = {
      ip,
      socketId: socket.id,
      lastSeen: Date.now()
    };
    console.log(`Geregistreerd: ${boxId} (${client})`);

    // Ack back to registrant
    socket.emit("register_ack", { success: true });

    // Notify all UIs of new device
    io.emit("device-connected", { boxId, ip });
  });

  // Frontend updates settings for a box
  socket.on("update-settings", ({ boxId, settings }) => {
    if (!devices[boxId]) return;
    // Merge new settings
    commands[boxId] = { ...commands[boxId], ...settings };
    const payload = { boxId, ...commands[boxId] };

    // Send command to the specific RPi
    io.to(devices[boxId].socketId).emit("command", payload);
    console.log(`Sent to device ${boxId}:`, payload);

    // Broadcast to other frontends
    socket.broadcast.emit("command", payload);
  });

  // Heartbeat from RPi
  socket.on("heartbeat", ({ boxId }) => {
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });

  // Cleanup on disconnect
  socket.on("disconnect", () => {
    // Find if this socket belonged to a device
    const gone = Object.entries(devices).find(
      ([, info]) => info.socketId === socket.id
    );
    if (gone) {
      const [boxId] = gone;
      delete devices[boxId];
      delete commands[boxId];
      io.emit("device-disconnected", { boxId });
      console.log(`Device disconnected: ${boxId}`);
    }
  });
});

// Periodieke inactiviteits-check
setInterval(() => {
  const now = Date.now();
  for (const [boxId, info] of Object.entries(devices)) {
    if (now - info.lastSeen > 60_000) {
      delete devices[boxId];
      delete commands[boxId];
      io.emit("device-disconnected", { boxId });
      console.log(`Removed inactive device: ${boxId}`);
    }
  }
}, 30_000);

server.listen(PORT, () => {
  console.log(`Backend draait op http://0.0.0.0:${PORT}`);
});
