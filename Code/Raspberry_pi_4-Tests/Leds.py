import time
from rpi_ws281x import PixelStrip, Color, ws

# LED-strip configuratie voor SK6812 RGBW
LED_COUNT = 100       # Aantal LEDs in de strip
LED_PIN = 18          # GPIO-pin (controleer of deze PWM ondersteunt)
LED_FREQ_HZ = 800000  # Signaal frequentie in Hz
LED_DMA = 10          # DMA-kanaal
LED_BRIGHTNESS = 50   # Helderheid (0-255)
LED_INVERT = False    # Inverteren van het signaal indien nodig
LED_CHANNEL = 0       # PWM-kanaal (meestal 0)
strip_type = ws.SK6812_STRIP_RGBW  # Specificeer RGBW-strip

# Initialiseer de LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                     LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

def collor_led_strip(color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
    strip.show()

try:
    while True:
        print("Rode kleur")
        collor_led_strip(Color(255, 0, 0, 0))  # rood
        time.sleep(2)

        print("Groene kleur")
        collor_led_strip(Color(0, 255, 0, 0))  # groen
        time.sleep(2)

        print("Blauwe kleur")
        collor_led_strip(Color(0, 0, 255, 0))  # blauw
        time.sleep(2)

        print("Witte kleur")
        collor_led_strip(Color(0, 0, 0, 255))  # wit 
        time.sleep(2)

        print("LEDs uit")
        collor_led_strip(Color(0, 0, 0, 0))    # uit
        time.sleep(2)

except KeyboardInterrupt:
    collor_led_strip(Color(0, 0, 0, 0))
    print("LED-test gestopt")
