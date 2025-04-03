// src/socket.js
import { io } from 'socket.io-client'

const SOCKET_URL = 'http://localhost:4000'

const socket = io(SOCKET_URL, {
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  timeout: 10000
})

// Connection event handlers
socket.on('connect', () => {
  console.log('Connected to WebSocket server')
})

socket.on('disconnect', (reason) => {
  console.log(`Disconnected from WebSocket server: ${reason}`)
})

socket.on('connect_error', (error) => {
  console.error('WebSocket connection error:', error)
})

socket.on('reconnect_attempt', (attemptNumber) => {
  console.log(`Attempting to reconnect... (Attempt ${attemptNumber})`)
})

// Custom event handlers
socket.on('sensor_data', (data) => {
  console.log('Received sensor data:', data)
  // Handle sensor data updates
})

socket.on('effect_trigger', (data) => {
  console.log('Received effect trigger:', data)
  // Handle effect triggers
})

// Helper functions
const emit = (eventName, data) => {
  if (socket.connected) {
    socket.emit(eventName, data)
    return true
  }
  console.warn('Socket not connected. Message not sent.')
  return false
}

export default socket
export { emit }
