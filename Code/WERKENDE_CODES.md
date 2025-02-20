
## ultrasone met sample
 
om de ultrasone te verbinden met RPI4 hebben we een spannngsdelere gebruikt van 1.8kΩ en 3.9kΩ (je kunt ook andere waarden gebruiken zolang de verhouding klopt).

- ECHO van HC-SR04 → 3.9kΩ weerstand → GPIO 6 (Pin 31)
- ECHO van HC-SR04 → 1.8kΩ weerstand → GND van Raspberry Pi

| **HC-SR04 Pin** | **Raspberry Pi 4 Pin** | **Opmerking** |
|---------------|------------------|------------|
| **VCC**       | **5V (Pin 2 of 4)** | Voeding voor de sensor |
| **GND**       | **GND (Pin 6, 9, 14, etc.)** | Aarde |
| **TRIG**      | **GPIO 5 (Pin 29)** | Stuur een puls om meting te starten |
| **ECHO**      | **GPIO 6 (Pin 31) via spanningsdeler** | Meet de afstand, verlagen naar 3.3V! |



```python
import time
import pygame
import RPi.GPIO as GPIO  

# Ultrasone sensor pins
TRIG_PIN = 5  
ECHO_PIN = 6  

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer pygame voor geluid
pygame.mixer.init()

# Laad geluidssamples
sample1 = pygame.mixer.Sound("/home/RPI1/Downloads/a.mp3")
sample2 = pygame.mixer.Sound("/home/RPI1/Downloads/c.mp3")
sample3 = pygame.mixer.Sound("/home/RPI1/Downloads/e.mp3")

def meet_afstand():
    """Meet de afstand met de HC-SR04 sensor en retourneert deze in cm."""
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  # Stabiliseer de sensor

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time, stop_time = time.time(), time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    afstand = (elapsed_time * 34300) / 2  # Snelheid van geluid = 34300 cm/s
    return afstand

try:
    while True:
        afstand = meet_afstand()
        print(f"Afstand: {afstand:.2f} cm")

        if afstand < 30:
            sample1.play()
            print("Speelt sample 1 af")
        elif 30 <= afstand < 60:
            sample2.play()
            print("Speelt sample 2 af")
        elif afstand >= 60:
            sample3.play()
            print("Speelt sample 3 af")

        time.sleep(1)  # Wacht 1 seconde voor de volgende meting

except KeyboardInterrupt:
    print("Programma gestopt")
    GPIO.cleanup()
```
## ultrasone met leds

**LED**
| LED pin | RPI4 pin | 
|----------|----------|
| VCC  | 5V+   | Data 3   
| DIN   | GPIO18 (PWM0)
|  GND | 0V



```python
import time
import RPi.GPIO as GPIO
import pygame
from rpi_ws281x import PixelStrip, Color, ws

# GPIO-configuratie voor de HC-SR04
TRIG_PIN = 5  # GPIO 5 - Trigger
ECHO_PIN = 6  # GPIO 6 - Echo

# LED-strip configuratie voor SK6812 RGBW
LED_COUNT = 100       # Aantal LEDs
LED_PIN = 18          # GPIO-pin voor dataverkeer (zorg dat deze PWM ondersteunt)
LED_FREQ_HZ = 800000  # LED signaal frequentie in hertz (meestal 800kHz)
LED_DMA = 10          # DMA-kanaal om het signaal te genereren
LED_BRIGHTNESS = 50   # Helderheid (0-255)
LED_INVERT = False    # True als je een inverterende schakeling hebt
LED_CHANNEL = 0       # Meestal 0, tenzij je een alternatieve PWM-kanaal gebruikt

# LED-strip type als SK6812 RGBW
strip_type = ws.SK6812_STRIP_RGBW

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer pygame voor audio
pygame.mixer.init()

# Laad de audiobestanden
sample1 = pygame.mixer.Sound("/home/RPI1/Downloads/a.mp3")
sample2 = pygame.mixer.Sound("/home/RPI1/Downloads/c.mp3")
sample3 = pygame.mixer.Sound("/home/RPI1/Downloads/e.mp3")  

# Initialiseer de LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                     LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

def set_all_leds(color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
    strip.show()

def measure_distance():
    """ Meet de afstand met de HC-SR04 en retourneert deze in cm. """
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  # Stabilisatie

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time, stop_time = time.time(), time.time()

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

        # Geluid afspelen op basis van afstandswaarde
        if distance < 30:
            short_sound.play()  # Speel korte sound af bij kleine afstand
            print("Speelt sample 1 af")
        elif 30 <= distance < 60:
            medium_sound.play()  # Speel een ander geluid af bij middellange afstand
            print("Speelt sample 2 af")
        elif distance >= 60:
            long_sound.play()  # Speel lang geluid bij grote afstand
            print("Speelt sample 3 af")

        # LEDs aansturen op basis van afstandswaarde
        leds_to_light = int(distance / 1.5)  # 1.5 cm per LED
        print(f"Aantal LEDs aan: {leds_to_light}")

        for i in range(LED_COUNT):
            if i < leds_to_light:
                strip.setPixelColor(i, Color(255, 255, 0, 0))  # Geel licht
            else:
                strip.setPixelColor(i, Color(0, 0, 0, 0))  # LED uitzetten

        strip.show()
        time.sleep(0.1)  # Kleine pauze om herhaalde metingen te vermijden

except KeyboardInterrupt:
    print("Programma gestopt")
    set_all_leds(Color(0, 0, 0, 0))  # Alle LEDs uitzetten
    GPIO.cleanup()
```
