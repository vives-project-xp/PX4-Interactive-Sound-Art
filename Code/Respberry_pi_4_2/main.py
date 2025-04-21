import time
import threading
import json
import numpy as np
import RPi.GPIO as GPIO
import socketio
from rpi_ws281x import PixelStrip, ws, Color
from led_effects import (
    effect_solid,
    effect_puls,
    effect_rainbow,
    effect_chase,
    effect_fire,
    effect_sparkle,
    IdleEffect
)

# --- Configuratie ---
box_id = "1"                                 # Uniek ID van deze RPI-box
TAILSCALE_IP = "100.65.86.118"              # Lokale IP-adres van de Pi
BACKEND_URL = "http://sound-art:4000"       # WebSocket-server URL

# Sensor pins
TRIG_PIN = 5
ECHO_PIN = 6

# LED strip instellingen
LED_COUNT = 63
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 0
STRIP_TYPE = ws.SK6812_STRIP_RGBW

# Statusbestand (optioneel)
STATUS_FILE = "/home/RPI2/Documents/txtFile/status.json"

# Globals
current_color = "#FFFFFF"
current_effect = "solid"
current_instrument = "guitar"
idle_mode = False
last_valid_distance = 0

def setup_hardware():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    # LED strip init
    strip = PixelStrip(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
        LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
        strip_type=STRIP_TYPE
    )
    strip.begin()
    return strip

strip = setup_hardware()
distance_buffer = np.zeros(5)

# --- Sensor en LED-logica ---
def measure_distance():
    """Meet afstand met ultrasoon sensor en return gefilterde waarde."""
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.001)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Puls-detectie
    start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300) / 2

    # Buffer voor gladstrijken
    global distance_buffer
    distance_buffer = np.roll(distance_buffer, -1)
    distance_buffer[-1] = distance
    filtered = np.mean(distance_buffer)
    return max(5, min(filtered, LED_COUNT * 1.6))


def get_level(distance):
    """Bepaal geluidsniveau aan de hand van afstand."""
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


def write_status_to_file(distance):
    """Schrijf instrument- en geluidsstatus naar JSON."""
    status = {
        "instrument": current_instrument,
        "sound_level": get_level(distance),
        "sound_stop": idle_mode
    }
    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(status, f)
    except Exception as e:
        print("Error writing status:", e)


def update_leds(count):
    """Update LED-strip aan de hand van huidige effectinstellingen."""
    if current_effect == "solid":
        effect_solid(strip, count, current_color)
    elif current_effect == "puls":
        effect_puls(strip, count, current_color)
    elif current_effect == "rainbow":
        effect_rainbow(strip, count)
    elif current_effect == "chase":
        effect_chase(strip, count, current_color)
    elif current_effect == "fire":
        effect_fire(strip, count)
    elif current_effect == "sparkle":
        effect_sparkle(strip, count, current_color)
    else:
        effect_solid(strip, count, current_color)


def distance_monitor():
    """Continue meten en updaten van LEDs, schakel na idle-tijd naar idle mode."""
    global last_valid_distance, idle_mode, current_instrument
    idle_effect = IdleEffect(strip, idle_color=(255,255,0))
    idle_start = None

    try:
        while True:
            dist = measure_distance()

            # Idle detectie
            if dist > last_valid_distance + 15:
                if idle_start is None:
                    idle_start = time.time()
                elif time.time() - idle_start >= 10:
                    idle_mode = True
                    current_instrument = "Stop"
            else:
                last_valid_distance = dist
                idle_start = None
                idle_mode = False

            leds_on = int(dist / 1.6)
            if idle_mode:
                idle_effect.update()
            else:
                update_leds(leds_on)

            write_status_to_file(dist)
            time.sleep(0.005)
    except KeyboardInterrupt:
        print("Stopping, cleanup...")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0,0))
        strip.show()
        GPIO.cleanup()

# --- WebSocket-client ---
sio = socketio.Client()

def send_heartbeat():
    while True:
        sio.emit('heartbeat', {'boxId': box_id})
        time.sleep(15)


@sio.event
def connect():
    print("Connected to backend")
    sio.emit('register', {'boxId': box_id, 'ip': TAILSCALE_IP, 'client': 'device'})


@sio.on('command')
def on_command(data):
    """Verwerk inkomende command: update globals en log."""
    global current_color, current_effect, current_instrument
    current_color = data.get('color', current_color)
    current_effect = data.get('effect', current_effect)
    current_instrument = data.get('instrument', current_instrument)
    print(f"Command ontvangen: {data}")


@sio.event
def disconnect():
    print("Disconnected from backend")

# --- Main ---
if __name__ == '__main__':
    # Start sensorloop
    threading.Thread(target=distance_monitor, daemon=True).start()
    # Start heartbeat
    threading.Thread(target=send_heartbeat, daemon=True).start()
    # Connect en block
    sio.connect(BACKEND_URL)
    sio.wait()