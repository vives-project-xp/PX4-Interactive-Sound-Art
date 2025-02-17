import time
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color, ws

# LED-strip configuratie voor SK6812 RGBW
LED_COUNT = 100       # Aantal LEDs
LED_PIN = 18          # GPIO-pin voor dataverkeer (zorg dat deze PWM ondersteunt)
LED_FREQ_HZ = 800000  # LED signaal frequentie in hertz (meestal 800kHz)
LED_DMA = 10          # DMA-kanaal om het signaal te genereren
LED_BRIGHTNESS = 50   # Helderheid (0-255)
LED_INVERT = False    # True als je een inverterende schakeling hebt
LED_CHANNEL = 0       # Meestal 0, tenzij je een alternatieve PWM-kanaal gebruikt

# ledstrip type als SK6812 RGBW
strip_type = ws.SK6812_STRIP_RGBW

# AfstandsSensor configuratie
TRIG_PIN = 5  # Trigger op GPIO 5
ECHO_PIN = 6  # Echo op GPIO 6
CM_LIGHT = 1.5  # Aantal cm per LED +-

TimeOuteCounter = 0

# GPIO instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer de LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                     LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()


def set_all_leds(color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
    strip.show()

def measure_distance():

    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Omrekenen naar cm
    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Afstand: {distance:.2f} cm")

        leds_to_light = int(distance / CM_LIGHT)
        print(f"Aantal LEDs aan: {leds_to_light}")


        ## Als de sensor 5sec lang niets ziet valt de ledstrip uit
        if distance > 177:
            TimeOuteCounter += 1
        else:
            TimeOuteCounter = 0

        if TimeOuteCounter < 20:
            for i in range(LED_COUNT):
                if i < leds_to_light:
                    strip.setPixelColor(i, Color(255, 255, 0, 0))
                else:
                    strip.setPixelColor(i, Color(0, 0, 0, 0))
        else:
            set_all_leds(Color(0, 0, 0, 0))

        strip.show()
        time.sleep(0.25)

except KeyboardInterrupt:
    print("Programma gestopt")
    set_all_leds(Color(0, 0, 0, 0))
    GPIO.cleanup()
