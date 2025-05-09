import { io } from "socket.io-client";

const socket = io("http://api.soundart.devbitapp.be", { autoConnect: false });

socket.on("connect_error", (err) => {
  console.warn("Socket.IO connect error:", err);
});

export default {
  on(event, cb)     { socket.on(event, cb); },
  off(event, cb)    { socket.off(event, cb); },
  emit(event, data) { socket.emit(event, data); },
  connect()         { socket.connect(); },
  disconnect()      { socket.disconnect(); }
};
