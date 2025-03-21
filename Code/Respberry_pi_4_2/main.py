#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import time, threading, json, numpy as np, RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import (effect_solid, effect_puls, effect_rainbow, effect_chase, 
                         effect_fire, effect_sparkle, IdleEffect)
import socketio  # Socket.IO client

app = Flask(__name__)
CORS(app)

# --- LED/Sensor Settings ---
TRIG_PIN = 5
ECHO_PIN = 6

LED_COUNT = 100
LED_PIN = 18
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

# Globale LED-instellingen met standaardwaarden
current_color = "#FFFF00"      # Default geel
current_effect = "solid"       # Options: "solid", "puls", "rainbow", "chase", "fire", "sparkle", etc.
current_instrument = "guitar"  # Default instrument

status_file = "/home/RPI2/Documents/txtFile/status.json"

def load_status():
    global current_instrument, current_color, current_effect
    try:
        with open(status_file, "r") as file:
            status = json.load(file)
            current_instrument = status.get("instrument", "guitar")
            current_color = status.get("color", "#FFFF00")
            current_effect = status.get("effect", "solid")
            print("Loaded status from file:", status)
    except Exception as e:
        print("Geen status gevonden, gebruik default settings", e)

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
    status = {
        "distance": distance,
        "instrument": current_instrument,
        "color": current_color,
        "effect": current_effect
    }
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
    idle_mode = False
    idle_start = None
    idle_effect = None
    try:
        while True:
            distance = measure_distance()
            leds_to_light = int(distance / 1.5)
            if leds_to_light > 99:
                if idle_start is None:
                    idle_start = time.time()
                elif time.time() - idle_start >= 10:
                    idle_mode = True
                    if idle_effect is None:
                        idle_effect = IdleEffect(strip, idle_color=(255, 255, 0))
            else:
                idle_start = None
                idle_mode = False
                idle_effect = None
                update_leds(distance)
            if idle_mode and idle_effect is not None:
                idle_effect.update()
            write_status_to_file(distance)
            time.sleep(0.005)
    except KeyboardInterrupt:
        print("Program stopped")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        strip.show()
        GPIO.cleanup()

# Flask endpoint om de huidige instellingen op te halen
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({
        "instrument": current_instrument,
        "color": current_color,
        "effect": current_effect
    })

# Socket.IO Client voor WebSocket-registratie en commando-ontvangst
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to backend via WebSocket")
    box_id = "box1"
    tailscale_ip = "100.65.86.118"
    sio.emit("register", {"boxId": box_id, "ip": tailscale_ip})
    # Start een thread om periodiek een heartbeat te sturen
    def send_heartbeat():
        while True:
            sio.emit("heartbeat", {"boxId": box_id})
            time.sleep(15)
    threading.Thread(target=send_heartbeat, daemon=True).start()

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
    backend_ws_url = "http://sound-art:4000"
    try:
        sio.connect(backend_ws_url)
    except Exception as e:
        print("Error connecting to backend via WebSocket:", e)

if __name__ == "__main__":
    load_status()
    # Start de afstandsmonitor op een aparte thread
    thread = threading.Thread(target=distance_monitor, daemon=True)
    thread.start()
    connect_to_backend()
    # Start de Flask server (beschikbaar op poort 5000)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
