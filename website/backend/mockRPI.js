// This file can be used for at home testing, this replicates an rpi

import { io } from 'socket.io-client';

const BOX_ID = process.env.BOX_ID || 'mock1';
const IP = '127.0.0.1';

const socket = io('http://localhost:4000');

// Initial state for the mock RPI
const initialState = {
  boxId: BOX_ID,
  isOn: true,
  color: '#FF0000',
  effect: 'solid',
  instrument: 'Gitaar',
  volume: 50
};

socket.on('connect', () => {
  console.log(`MockPi connected as boxId=${BOX_ID}`);
  socket.emit('register', { boxId: BOX_ID, ip: IP, client: 'rpi' });

  // Send initial state after registration
  setTimeout(() => {
    console.log('Sending initial state to server');
    socket.emit('update-settings', { 
      boxId: BOX_ID, 
      settings: initialState 
    });
  }, 1000);

  // send heartbeats every 20s so server keeps us alive
  setInterval(() => {
    socket.emit('heartbeat', { boxId: BOX_ID });
  }, 20000);
});

socket.on('command', (data) => {
  console.log('Received command from server:', data);
  // Here you could simulate LEDs or sound logic...
});

socket.on('disconnect', () => {
  console.log('MockPi disconnected');
});
