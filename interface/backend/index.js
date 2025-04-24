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

// In‐memory storage
const devices = {};   // { [boxId]: { ip, socketId, lastSeen } }
const commands = {};  // { [boxId]: { isOn, color, effect, instrument, … } }

app.use(cors());
app.use(express.json());

io.on("connection", (socket) => {
  console.log("🔌 New socket:", socket.id);

  // 1) Immediately send current device list to the newcomer
  const list = Object.entries(devices).map(([boxId, info]) => ({
    boxId,
    ip: info.ip
  }));
  socket.emit("devices-list", list);

  // 2) Registration handler (front-end vs. Pi)
  socket.on("register", ({ boxId, ip, client }) => {
    if (client === "frontend") {
      console.log(`👩‍💻 Front-end registered: ${socket.id}`);
      return;
    }
    // must be a Pi
    if (!boxId || !ip) return;
    devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
    console.log(`🎵 Pi registered → boxId=${boxId} ip=${ip}`);

    // ack & notify all front-ends about the new box
    socket.emit("register_ack", { success: true });
    io.emit("device-connected", { boxId, ip });
  });

  // 3) Front-end pushes a setting update
  socket.on("update-settings", ({ boxId, settings }) => {
    if (!devices[boxId]) return;
    // merge into our commands store
    commands[boxId] = { ...commands[boxId], ...settings };
    const payload = { boxId, ...commands[boxId] };

    // a) send to the specific Pi
    io.to(devices[boxId].socketId).emit("command", payload);
    // b) broadcast to ALL clients (so every open UI sees it)
    io.emit("command", payload);

    console.log(`Update box ${boxId}:`, payload);
  });

  // 4) Pi heartbeat to stay alive
  socket.on("heartbeat", ({ boxId }) => {
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });

  // 5) Clean up on disconnect
  socket.on("disconnect", () => {
    // Was it a Pi?
    const gone = Object.entries(devices).find(
      ([, info]) => info.socketId === socket.id
    );
    if (gone) {
      const [boxId] = gone;
      delete devices[boxId];
      delete commands[boxId];
      io.emit("device-disconnected", { boxId });
      console.log(`Pi disconnected: boxId=${boxId}`);
    }
  });
});

// Periodically remove stale Pis
setInterval(() => {
  const now = Date.now();
  for (const [boxId, info] of Object.entries(devices)) {
    if (now - info.lastSeen > 60_000) {
      delete devices[boxId];
      delete commands[boxId];
      io.emit("device-disconnected", { boxId });
      console.log(`Removed inactive box: ${boxId}`);
    }
  }
}, 30_000);

server.listen(PORT, () => {
  console.log(`Backend listening on http://0.0.0.0:${PORT}`);
});