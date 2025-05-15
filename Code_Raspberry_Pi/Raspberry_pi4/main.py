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

# --- Flask App & Socket.IO Server Setup ---
app = Flask(__name__)
CORS(app)
socketio_server = SocketIO(app, cors_allowed_origins="*")

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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

strip = PixelStrip(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
    strip_type=strip_type
)
strip.begin()

window_size = 5
distance_buffer = np.zeros(window_size)
default_max_distance = 150.0  # 1.50 m maximum for responsiveness

# Global LED and state settings
current_color = "#FFFFFF"
current_effect = "solid"
current_instrument = "Guitar"
current_device_isOn = True
current_volume = 100

idle_mode = True
last_valid_distance = 0

status_file = "/home/RPI2/Documents/txtFile/status.json"
box_id = "2"
sound_isOff = False

def measure_distance(timeout=0.01):
    """
    Meet afstand met korte echo-timeout (10 ms). 
    Alles boven 1.50 m wordt direct op 1.50 m gezet.
    """
    # Trigger pulse
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.001)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start = time.time()
    # Wacht op rising edge, max timeout
    while GPIO.input(ECHO_PIN) == 0 and (time.time() - start) < timeout:
        pass
    if GPIO.input(ECHO_PIN) == 0:
        raw = default_max_distance
    else:
        echo_start = time.time()
        # Wacht op falling edge, max timeout
        while GPIO.input(ECHO_PIN) == 1 and (time.time() - echo_start) < timeout:
            pass
        if GPIO.input(ECHO_PIN) == 1:
            raw = default_max_distance
        else:
            elapsed = time.time() - echo_start
            raw = (elapsed * 34300) / 2  # in cm

    # Direct clippen van extreme waarden
    if raw > default_max_distance or raw < 5:
        raw = default_max_distance

    # Buffer en median-filter voor robuustheid
    global distance_buffer
    distance_buffer = np.roll(distance_buffer, -1)
    distance_buffer[-1] = raw
    filtered = float(np.median(distance_buffer))

    return max(5, min(filtered, default_max_distance))

def write_status_to_file(distance):
    status = {
        "instrument": current_instrument,
        "sound_level": get_level(distance),
        "sound_stop": sound_isOff,            # schrijf een boolean
        "volume": int(current_volume)            # zorg dat het een int is
    }
    try:
        with open(status_file, "w") as file:
            json.dump(status, file)
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


def get_level(distance):
    if distance < 10:
        return 1
    elif distance < 20:
        return 2
    elif distance < 30:
        return 3
    elif distance < 40:
        return 4
    elif distance < 50:
        return 5
    elif distance < 60:
        return 6
    elif distance < 70:
        return 7
    else:
        return 8


def distance_monitor():
    global last_valid_distance, idle_mode, prev_idle_mode, sound_isOff, current_device_isOn
    idle_start = None
    idle_effect = IdleEffect(strip, idle_color=(255, 255, 0))

    try:
        while True:
            # Device uit?
            if not current_device_isOn:
                sound_isOff = True
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0, 0, 0, 0))
                strip.show()
                write_status_to_file(last_valid_distance)
                time.sleep(0.005)
                continue

            distance = measure_distance()
            # Idle-detectie
            if distance > last_valid_distance + 15:
                distance = last_valid_distance
                if idle_start is None:
                    idle_start = time.time()
                if time.time() - idle_start >= 60:
                    idle_mode = True
                    current_instrument = "Stop"
            else:
                last_valid_distance = distance
                idle_start = None
                idle_mode = False

            leds_to_light = int(distance / 1.6)

            if idle_mode:
                sound_isOff = True
                # *** overgang naar idle: reset en zet alles uit ***
                if not prev_idle_mode:
                    # alle LEDs uit
                    for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 0, 0, 0))
                    strip.show()
                    # reset animatie
                    idle_effect.reset()
                prev_idle_mode = True
                idle_effect.update()
            else:
                prev_idle_mode = False
                sound_isOff = False
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
    tailscale_ip = "100.65.86.118"
    sio.emit("register", {"boxId": box_id, "ip": tailscale_ip})

@sio.event
def disconnect():
    print("Disconnected from backend")

@sio.on("command")
def command_handler(data):
    global current_color, current_effect, current_instrument, current_volume, current_device_isOn
    current_color = data.get("color", "#FFFFFF")
    current_effect = data.get("effect", "solid")
    current_instrument = data.get("instrument", "unknown")
    current_volume = data.get("volume", 0)
    current_device_isOn = data.get("isOn", False)
    print(f"WebSocket Command -> Instrument: {current_instrument} | Color: {current_color} | Effect: {current_effect} | Volume: {current_volume} | Device is On: {current_device_isOn}")

def send_heartbeat():
    while True:
        try:
            sio.emit("heartbeat", {"boxId": box_id})
            print("Heartbeat sent")
        except Exception as e:
            print("Error sending heartbeat:", e)
        time.sleep(15)

def connect_to_backend():
    backend_ws_url = "https://api.soundart.devbitapp.be"
    try:
        sio.connect(backend_ws_url)
    except Exception as e:
        print("Error connecting to backend via WebSocket:", e)

# --- Main Execution ---
if __name__ == "__main__":
    thread_monitor = threading.Thread(target=distance_monitor, daemon=True)
    thread_monitor.start()
    connect_to_backend()
    thread_heartbeat = threading.Thread(target=send_heartbeat, daemon=True)
    thread_heartbeat.start()
    socketio_server.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)