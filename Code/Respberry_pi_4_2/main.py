from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading
import math
import json
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color, ws
import numpy as np
from led_effects import effect_solid, effect_puls, effect_rainbow, effect_chase, effect_fire, effect_sparkle

app = Flask(__name__)
CORS(app)

# Instellingen afstandssensor
TRIG_PIN = 5
ECHO_PIN = 6

# LED-strip instellingen
LED_COUNT = 100
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 200
LED_INVERT = False
LED_CHANNEL = 0
strip_type = ws.SK6812_STRIP_RGBW

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer de LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                   LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

# Moving average filter
window_size = 5
distance_buffer = np.zeros(window_size)

# Globale instellingen
current_color = "#FFFF00"       # Standaard kleur: geel
current_effect = "solid"        # Mogelijke waarden: "solid", "puls", "rainbow"
current_instrument = "guitar"  # Wordt meegegeven via POST

# Pad voor statusbestand (afstand en instrument)
status_file = "/home/RPI2/Documents/txtFile/status.json"

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
        "instrument": current_instrument
    }
    try:
        with open(status_file, "w") as file:
            file.write(json.dumps(status))
    except Exception as e:
        print("Fout bij schrijven status:", e)

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

@app.route("/update", methods=["POST"])
def update():
    global current_color, current_effect, current_instrument
    data = request.json
    current_color = data.get("color", "#FFFFFF")
    current_effect = data.get("effect", "solid")
    current_instrument = data.get("instrument", "unknown")
    print(f"Instrument: {current_instrument} | Nieuwe kleur: {current_color} | Nieuw effect: {current_effect}")
    return jsonify({"message": "LED instellingen updated!"})

def distance_monitor():
    try:
        while True:
            distance = measure_distance()
            update_leds(distance)
            write_status_to_file(distance)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Programma gestopt")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        strip.show()
        GPIO.cleanup()

if __name__ == "__main__":
    thread = threading.Thread(target=distance_monitor, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)