#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO  # (Not used for server here but needed if you want to add SocketIO events later)
import time, threading, json, numpy as np, RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import effect_solid, effect_puls, effect_rainbow, effect_chase, effect_fire, effect_sparkle
import socketio  # Socket.IO client
import requests

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)

# --- LED/Sensor Settings ---
# Ultrasonic sensor pins
TRIG_PIN = 5
ECHO_PIN = 6

# LED-strip settings
LED_COUNT = 100
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 50
LED_INVERT = False
LED_CHANNEL = 0
strip_type = ws.SK6812_STRIP_RGBW

# Setup GPIO for sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize the LED strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                   LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

# Moving average filter for distance
window_size = 5
distance_buffer = np.zeros(window_size)

# Global LED settings
current_color = "#FFFF00"      # Default yellow
current_effect = "solid"       # Options: "solid", "puls", "rainbow"
current_instrument = "guitar"  # Default instrument

# (Optional) Status file path
status_file = "/home/RPI2/Documents/txtFile/status.json"

# --- Functions for Sensor and LED Control ---
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
    return max(5, min(filtered_distance, LED_COUNT * 1.5))

def write_status_to_file(distance):
    status = {"distance": distance, "instrument": current_instrument}
    try:
        with open(status_file, "w") as file:
            file.write(json.dumps(status))
    except Exception as e:
        print("Error writing status:", e)

def update_leds(distance):
    leds_to_light = int(distance / 1.5)
    
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
    try:
        while True:
            distance = measure_distance()
            update_leds(distance)
            write_status_to_file(distance)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        strip.show()
        GPIO.cleanup()

# --- Socket.IO Client for WebSocket Registration & Command Receiving ---
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to backend via WebSocket")
    # Register with the backend using your boxId and Tailscale IP.
    box_id = "box1"
    tailscale_ip = "100.65.86.118"  # Replace with your Pi's actual Tailscale IP
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

def connect_to_backend():
    # Replace <BACKEND_TAILSCALE_IP> with your backend's Tailscale IP or hostname.
    backend_ws_url = "http://sound-art:4000"
    try:
        sio.connect(backend_ws_url)
    except Exception as e:
        print("Error connecting to backend via WebSocket:", e)

# --- Main Execution ---
if __name__ == "__main__":
    # Start the distance monitor in a background thread
    thread = threading.Thread(target=distance_monitor, daemon=True)
    thread.start()
    
    # Connect to the backend via WebSocket for real-time commands
    connect_to_backend()
    
    # Start the Flask HTTP server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
