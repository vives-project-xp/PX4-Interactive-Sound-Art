import { io } from 'socket.io-client'

const socket = io('http://localhost:4000') // adjust URL if needed

export default socket