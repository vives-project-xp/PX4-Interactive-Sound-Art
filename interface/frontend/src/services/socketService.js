import { io } from "socket.io-client";

// Verbind met je backend, maar registreer pas nadat de socket echt connect
const socket = io("http://localhost:4000", { autoConnect: false });

socket.on("connect", () => {
  // 1x registreren zodra de verbinding staat
  socket.emit("register", { client: "frontend" });
});

// Optioneel: reconnect logic, error‑handling…
socket.on("connect_error", (err) => {
  console.warn("Socket.IO connect error:", err);
});

// Exporteer alle methodes die je nodig hebt
export default {
  // luister naar binnenkomende events
  on(event, callback) {
    socket.on(event, callback);
  },

  // stop met luisteren
  off(event, callback) {
    socket.off(event, callback);
  },

  // stuur een event
  emit(event, data) {
    socket.emit(event, data);
  },

  // maak expliciet de verbinding
  connect() {
    socket.connect();
  },

  // sluit de socket weer af
  disconnect() {
    socket.disconnect();
  }
};
