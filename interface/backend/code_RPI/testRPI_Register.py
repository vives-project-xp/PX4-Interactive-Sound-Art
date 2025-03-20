from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time, threading, numpy as np, RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import effect_solid, effect_puls, effect_rainbow
import socketio  # Client for Socket.IO
import requests

# Flask app voor eventuele HTTP endpoints (optioneel)
app = Flask(__name__)
CORS(app)
socketio_server = SocketIO(app, cors_allowed_origins="*")

# LED en sensor instellingen (zoals eerder)
TRIG_PIN = 5
ECHO_PIN = 6
LED_COUNT = 100
LED_PIN = 12
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 50
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
current_color = "#FFFF00"
current_effect = "solid"  # opties: "solid", "puls", "rainbow"

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

def update_leds(distance):
    leds_to_light = int(distance / 1.5)
    if current_effect == "solid":
        effect_solid(strip, leds_to_light, current_color)
    elif current_effect == "puls":
        effect_puls(strip, leds_to_light, current_color)
    elif current_effect == "rainbow":
        effect_rainbow(strip, leds_to_light)
    else:
        effect_solid(strip, leds_to_light, current_color)

def distance_monitor():
    try:
        while True:
            distance = measure_distance()
            update_leds(distance)
            time.sleep(0.1)
    except KeyboardInterrupt:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        strip.show()
        GPIO.cleanup()

# Handle incoming WebSocket command events from the backend
def on_command(data):
    global current_color, current_effect
    current_color = data.get("color", "#FFFFFF")
    current_effect = data.get("effect", "solid")
    instrument = data.get("instrument", "unknown")
    print(f"WebSocket command received -> Instrument: {instrument} | Color: {current_color} | Effect: {current_effect}")

# Create a Socket.IO client and connect to the central backend
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to backend via WebSocket")
    # Register this device with the backend via WebSocket
    box_id = "box1"
    tailscale_ip = "100.98.149.108"  # Your Pi's Tailscale IP
    sio.emit("register", {"boxId": box_id, "ip": tailscale_ip})

@sio.event
def disconnect():
    print("Disconnected from backend")

@sio.on("command")
def command_handler(data):
    on_command(data)

def connect_to_backend():
    # Replace <BACKEND_TAILSCALE_IP> with the Tailscale IP or hostname of your backend server
    backend_ws_url = "http://<BACKEND_TAILSCALE_IP>:4000"
    try:
        sio.connect(backend_ws_url)
    except Exception as e:
        print("Error connecting to backend:", e)

if __name__ == "__main__":
    # Start the distance monitor in a thread
    thread = threading.Thread(target=distance_monitor, daemon=True)
    thread.start()
    
    # Connect to the backend via WebSocket
    connect_to_backend()
    
    # Start Flask server for HTTP endpoints (if needed)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
