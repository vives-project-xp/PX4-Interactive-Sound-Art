#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time, threading, json, numpy as np, RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import (effect_solid, effect_puls, effect_rainbow, effect_chase, 
                         effect_fire, effect_sparkle, IdleEffect)
import socketio  # Socket.IO client
import requests

# --- Flask App & Socket.IO Setup ---
app = Flask(__name__)
CORS(app)
socketio_server = SocketIO(app, cors_allowed_origins="*")

@socketio_server.on('test_event')
def handle_test_event(data):
    print("Ontvangen test_event met data:", data)
    emit('response', {'data': 'Test response from server'})

# --- LED/Sensor Instellingen ---
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

# Globale LED instellingen
current_color = "#FFFFFF"
current_effect = "solid"
current_instrument = "guitar"

status_file = "/home/RPI2/Documents/txtFile/status.json"
box_id = "1"  # Globale box identificatie

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
        print("Fout bij wegschrijven status:", e)

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
    threshold = 63

    try:
        while True:
            distance = measure_distance()
            leds_to_light = int(distance / 1.6)
            
            if leds_to_light >= threshold:
                if idle_start is None:
                    idle_start = time.time()
                if time.time() - idle_start >= 10:
                    idle_mode = True
            else:
                idle_start = None
                idle_mode = False
            
            if idle_mode:
                idle_effect.update()
            else:
                update_leds(leds_to_light)
            
            write_status_to_file(distance)
            time.sleep(0.005)
            
    except KeyboardInterrupt:
        print("Programma gestopt")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        strip.show()
        GPIO.cleanup()

# --- Socket.IO Client ---
sio = socketio.Client()

@sio.event
def connect():
    print("Verbonden met backend via WebSocket")
    tailscale_ip = "100.65.86.118"
    sio.emit("register", {"boxId": box_id, "ip": tailscale_ip})

@sio.event
def disconnect():
    print("Verbroken met backend")

@sio.on("command")
def command_handler(data):
    global current_color, current_effect, current_instrument
    current_color = data.get("color", "#FFFFFF")
    current_effect = data.get("effect", "solid")
    current_instrument = data.get("instrument", "unknown")
    print(f"WebSocket Command -> Instrument: {current_instrument} | Color: {current_color} | Effect: {current_effect}")

def send_heartbeat():
    while True:
        try:
            sio.emit("heartbeat", {"boxId": box_id})
            print("Heartbeat verzonden")
        except Exception as e:
            print("Fout bij het verzenden van heartbeat:", e)
        time.sleep(15)

def connect_to_backend():
    backend_ws_url = "http://sound-art:4000"
    try:
        sio.connect(backend_ws_url)
    except Exception as e:
        print("Fout bij verbinden met backend via WebSocket:", e)

# --- Main ---
if __name__ == "__main__":
    thread_monitor = threading.Thread(target=distance_monitor, daemon=True)
    thread_monitor.start()
    
    connect_to_backend()
    
    thread_heartbeat = threading.Thread(target=send_heartbeat, daemon=True)
    thread_heartbeat.start()
    
    socketio_server.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
