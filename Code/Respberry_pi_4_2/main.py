#!/usr/bin/env python3#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time, threading, json, numpy as np, RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import (effect_solid, effect_puls, effect_rainbow, effect_chase, 
                         effect_fire, effect_sparkle, IdleEffect)
import socketio  # Socket.IO client
import requests

# --- Flask App & Socket.IO Server Setup ---
app = Flask(__name__)
CORS(app)
socketio_server = SocketIO(app, cors_allowed_origins="*")

# (Optional) Example Socket.IO event handler for clients connecting to this server
@socketio_server.on('test_event')
def handle_test_event(data):
    print("Received test_event with data:", data)
    emit('response', {'data': 'Test response from server'})

# --- LED/Sensor Settings ---
TRIG_PIN = 5
ECHO_PIN = 6

LED_COUNT = 63
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 0
strip_type = ws.SK6812_STRIP_RGBW

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                   LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

window_size = 5
distance_buffer = np.zeros(window_size)

# Global LED settings
current_color = "#FFFFFF"      # Default yellow
current_effect = "solid"       # Options: "solid", "puls", "rainbow", "chase", "fire", "sparkle", etc.
current_instrument = "guitar"  # Default instrument

status_file = "/home/RPI2/Documents/txtFile/status.json"
box_id = "1"  # Global box identifier

def measure_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.001)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    start_time, stop_time = time.time(), time.time()
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    global distance_buffer
    distance_buffer = np.roll(distance_buffer, -1)
    distance_buffer[-1] = distance
    filtered_distance = np.mean(distance_buffer)
    return max(5, min(filtered_distance, LED_COUNT * 1.6))

def write_status_to_file(distance):
    status = {"distance": distance, "instrument": current_instrument}
    try:
        with open(status_file, "w") as file:
            file.write(json.dumps(status))
    except Exception as e:
        print("Error writing status:", e)

def update_leds(leds_to_light):
    if current_effect == "solid":
        effect_solid(strip, leds_to_light, current_color)
    elif current_effect == "puls":
        effect_puls(strip, leds_to_light, current_color)
    elif current_effect == "rainbow":
        effect_rainbow(strip, leds_to_light)
    elif current_effect == "chase":
        effect_chase(strip, leds_to_light, current_color)
    elif current_effect == "fire":
        effect_fire(strip, leds_to_light)
    elif current_effect == "sparkle":
        effect_sparkle(strip, leds_to_light, current_color)
    else:
        effect_solid(strip, leds_to_light, current_color)

def distance_monitor():
    idle_start = None
    idle_mode = None
    idle_effect = IdleEffect(strip, idle_color=(255, 255, 0))
    threshold = 63  # Als leds_to_light >= threshold, dan wordt er geen hand gedetecteerd.

    try:
        while True:
            distance = measure_distance()
            leds_to_light = int(distance / 1.6)
            
            if leds_to_light >= threshold:
                # Als er lange tijd (60 sec) geen hand is, activeer idle mode
                if idle_start is None:
                    idle_start = time.time()
                if time.time() - idle_start >= 10:
                    idle_mode = True
            else:
                # Hand gedetecteerd: reset idle start en mode, en voer normale update uit
                idle_start = None
                idle_mode = False
            
            if idle_mode == True:
                idle_effect.update()
            else:
                update_leds(leds_to_light)
            
            write_status_to_file(distance)
            time.sleep(0.005)
            
    except KeyboardInterrupt:
        print("Program stopped")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        strip.show()
        GPIO.cleanup()

# --- Socket.IO Client for WebSocket Registration, Heartbeat & Command Receiving ---
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to backend via WebSocket")
    # Register the device with its box_id and IP (update IP if needed)
    tailscale_ip = "100.65.86.118"
    sio.emit("register", {"boxId": box_id, "ip": tailscale_ip})

@sio.event
def disconnect():
    print("Disconnected from backend")

@sio.on("command")
def command_handler(data):
    global current_color, current_effect, current_instrument
    current_color = data.get("color", "#FFFFFF")
    current_effect = data.get("effect", "solid")
    current_instrument = data.get("instrument", "unknown")
    print(f"WebSocket Command -> Instrument: {current_instrument} | Color: {current_color} | Effect: {current_effect}")

def send_heartbeat():
    """Periodically emit a heartbeat to the backend to indicate this device is still active."""
    while True:
        try:
            sio.emit("heartbeat", {"boxId": box_id})
            print("Heartbeat sent")
        except Exception as e:
            print("Error sending heartbeat:", e)
        time.sleep(15)  # Emit heartbeat every 15 seconds

def connect_to_backend():
    backend_ws_url = "http://sound-art:4000"
    try:
        sio.connect(backend_ws_url)
    except Exception as e:
        print("Error connecting to backend via WebSocket:", e)

# --- Main Execution ---
if __name__ == "__main__":
    # Start the distance monitor in a background thread
    thread_monitor = threading.Thread(target=distance_monitor, daemon=True)
    thread_monitor.start()
    
    # Connect to the central backend via WebSocket
    connect_to_backend()
    
    # Start the heartbeat thread so that the device remains registered
    thread_heartbeat = threading.Thread(target=send_heartbeat, daemon=True)
    thread_heartbeat.start()
    
    # Start the Flask app with Socket.IO support for incoming WebSocket connections
    socketio_server.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)