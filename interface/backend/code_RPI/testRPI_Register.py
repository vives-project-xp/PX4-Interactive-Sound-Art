from flask import Flask, request, jsonify
from flask_cors import CORS
import time, threading, numpy as np, RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import effect_solid, effect_puls, effect_rainbow
import requests  # nodig voor de registratie

app = Flask(__name__)
CORS(app)

# Instellingen afstandssensor
TRIG_PIN = 5
ECHO_PIN = 6

# LED-strip instellingen
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

# Globale instellingen voor LED's
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

@app.route("/update", methods=["POST"])
def update():
    global current_color, current_effect
    data = request.json
    current_color = data.get("color", "#FFFFFF")
    current_effect = data.get("effect", "solid")
    instrument = data.get("instrument", "unknown")
    print(f"Instrument: {instrument} | Nieuwe kleur: {current_color} | Nieuw effect: {current_effect}")
    return jsonify({"message": "LED instellingen updated!"})

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

def register_device():
    """
    Registreer de Raspberry Pi bij de centrale backend.
    Zorg ervoor dat Tailscale actief is en dat je het correcte Tailscale-IP gebruikt.
    """
    box_id = "box1"  # Unieke identificatie van deze box
    tailscale_ip = "10.10.2.48"  # Vervang dit met het daadwerkelijke Tailscale-IP van deze Pi
    backend_url = "http://<BACKEND_IP>:4000/register"  # Vervang <BACKEND_IP> met het IP/domein van de backend
    data = {
        "boxId": box_id,
        "ip": tailscale_ip
    }
    try:
        response = requests.post(backend_url, json=data)
        print("Registratie succesvol:", response.text)
    except Exception as e:
        print("Registratie mislukt:", e)

if __name__ == "__main__":
    # Registreer de Pi bij de backend
    register_device()
    # Start de afstandsmeting in een aparte thread
    thread = threading.Thread(target=distance_monitor, daemon=True)
    thread.start()
    # Start de Flask-server op poort 5000
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
