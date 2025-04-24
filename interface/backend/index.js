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

// In-memory opslag
const devices = {};
const commands = {};

app.use(cors());
app.use(express.json());

io.on("connection", (socket) => {
  console.log("Nieuwe socket-verbinding:", socket.id);

  // 1. Stuur huidige lijst devices
  const list = Object.entries(devices).map(([boxId, info]) => ({
    boxId,
    ip: info.ip
  }));
  socket.emit("devices-list", list);

  // 2. Registratie van frontend of RPi
  socket.on("register", ({ boxId, ip, client }) => {
    if (!boxId) return;
    devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
    console.log(`Geregistreerd: ${boxId} (${client})`);
    socket.emit("register_ack", { success: true });

    // Notify alle UIs
    io.emit("device-connected", { boxId, ip });
  });

  // 3. Frontend stuurt nieuwe instellingen
  socket.on("update-settings", ({ boxId, settings }) => {
    if (!devices[boxId]) return;
    commands[boxId] = { ...commands[boxId], ...settings };
    const payload = { boxId, ...commands[boxId] };

    // Naar RPi
    io.to(devices[boxId].socketId).emit("command", payload);
    console.log(`Sent to device ${boxId}:`, payload);

    // Broadcast naar andere frontends
    socket.broadcast.emit("command", payload);
  });

  // 4. Heartbeat van RPi
  socket.on("heartbeat", ({ boxId }) => {
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });

  // 5. Cleanup op disconnect
  socket.on("disconnect", () => {
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

// Periodieke inactieve‐check
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
