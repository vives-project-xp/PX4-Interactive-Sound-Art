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

// In-memory storage
const devices = {};   // { [boxId]: { ip, socketId, lastSeen } }
const commands = {};  // { [boxId]: { isOn, color, effect, instrument, … } }

app.use(cors());
app.use(express.json());

// Hello from backend
app.get("/", (req, res) => {
  res.json({ message: "Hello from the backend!" });
});

io.on("connection", (socket) => {
  console.log("New socket:", socket.id);

  // Send current device list to the newcomer
  const list = Object.entries(devices).map(([boxId, info]) => ({
    boxId,
    ip: info.ip
  }));
  socket.emit("devices-list", list);

  // Registration handler (front-end vs. Pi)
  socket.on("register", ({ boxId, ip, client }) => {
    if (client === "frontend") {
      // Front-ends join the 'frontends' room
      socket.join("frontends");
      console.log(`Front-end joined room: ${socket.id}`);
      return;
    }
    // Must be a Pi
    if (!boxId || !ip) return;
    devices[boxId] = { ip, socketId: socket.id, lastSeen: Date.now() };
    socket.join(`pi-${boxId}`);
    console.log(`Pi registered → boxId=${boxId}, joined room pi-${boxId}`);

    // Ack & notify all front-ends about the new box
    socket.emit("register_ack", { success: true });
    io.to("frontends").emit("device-connected", { boxId, ip });
  });

  // Front-end pushes a setting update
  socket.on("update-settings", ({ boxId, settings }) => {
    if (!devices[boxId]) return;

    // Merge into our commands store
    commands[boxId] = { ...commands[boxId], ...settings };
    const payload = { boxId, ...commands[boxId] };

    // Send only to the Pi in its room
    io.to(`pi-${boxId}`).emit("command", payload);

    // Send to all front-ends for UI updates
    io.to("frontends").emit("command", payload);

    console.log(`Update box ${boxId}:`, payload);
  });

  // Pi heartbeat to stay alive
  socket.on("heartbeat", ({ boxId }) => {
    if (devices[boxId]) {
      devices[boxId].lastSeen = Date.now();
    }
  });

  // Clean up on disconnect
  socket.on("disconnect", () => {
    // Was it a Pi?
    const gone = Object.entries(devices).find(
      ([, info]) => info.socketId === socket.id
    );
    if (gone) {
      const [boxId] = gone;
      delete devices[boxId];
      delete commands[boxId];
      io.to("frontends").emit("device-disconnected", { boxId });
      console.log(`Pi disconnected: boxId=${boxId}`);
    }
  });
});

// Periodically remove stale Pis
setInterval(() => {
  const now = Date.now();
  Object.entries(devices).forEach(([boxId, info]) => {
    if (now - info.lastSeen > 60000) {
      delete devices[boxId];
      delete commands[boxId];
      io.to("frontends").emit("device-disconnected", { boxId });
      console.log(`Removed inactive box: ${boxId}`);
    }
  });
}, 30000);

server.listen(PORT, () => {
  console.log(`Backend listening on http://0.0.0.0:${PORT}`);
});
