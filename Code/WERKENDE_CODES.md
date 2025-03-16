# Werkende code
## Algemene info
Voor iedere schakeling gebruiken we volgende pinconfiguratie.
| **HC-SR04 Pin** | **Raspberry Pi 4 Pin** | **Opmerking** |
|---------------|------------------|------------|
| **VCC**       | **5V (Pin 2)** | Voeding voor de sensor |
| **GND**       | **GND (Pin 6)** | GND van de HC-SR04 en de RPI4 moet verbonden zijn met elkaar|
| **TRIG**      | **GPIO 5 (Pin 29)** | Stuur een puls om meting te starten |
| **ECHO**      | **GPIO 6 (Pin 31) via spanningsdeler** | Meet de afstand, verlagen naar 3.3V! (GPIO pin werkt op 3,3V) |

## Samples laten afpselen aan de hand van een ultrasone sensor (HC-SR04)
 
Dit programma gebruikt een HC-SR04 ultrasone sensor om afstanden te meten en speelt een audiobestand af op basis van de gemeten afstand.

- Minder dan 30 cm → Speelt sample1.mp3
- 30 - 60 cm → Speelt sample2.mp3
- Meer dan 60 cm → Speelt sample3.mp3

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
## LEDs interactief laten meebewegen aan de hand van een ultrasone sensor (HC-SR04) 
Dit programma stuurt een **SK6812 RGBW LED-strip** aan de hand van de ultrasone sensor (HC-SR04).

### Werking:  
- **Minder dan 30 cm** → Laat een klein aantal LEDs branden.  
- **30 - 60 cm** →  Laat een middelgroot aantal LEDs branden.  
- **Meer dan 60 cm** →  Laat bijna alle LEDs branden.  

De LEDs reageren dynamisch op de afstand van het

### Opstelling
Bij dit programma/opstelling gebruiken we nog steeds dezelfde pinconfiguratie voor de ultrasone sensor hier boven. Nu komt er ook een LEDstrip bij, hiervoor gebruiken we volgende pinconfiguratie.
### LED-strip -> Raspberry Pi 4
| **LED-strip Pin** | **Raspberry Pi 4 Pin**       | **Opmerking**                      |
|------------------|-------------------------|--------------------------------|
| **VCC (5V)**    | **Externe 5V voeding**   | Niet direct op Raspberry Pi!  |
| **GND**         | **GND (Raspberry Pi en voeding delen GND)** | Gemeenschappelijke aarde |
| **DIN (Data In)** | **GPIO 18 (Pin 12)**    | (PWM0) Moet PWM ondersteunen!        |

### Programma
audio bestanden werken hier niet.
```python
import time
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color, ws
import numpy as np  # Voor moving average filter

# GPIO-configuratie voor de HC-SR04
TRIG_PIN = 5  # GPIO 5 - Trigger
ECHO_PIN = 6  # GPIO 6 - Echo

# LED-strip configuratie voor SK6812 RGBW
LED_COUNT = 100       # Aantal LEDs
LED_PIN = 18          # GPIO-pin voor dataverkeer (PWM)
LED_FREQ_HZ = 800000  # LED signaal frequentie (800kHz)
LED_DMA = 10          # DMA-kanaal
LED_BRIGHTNESS = 50   # Start helderheid (0-255)
LED_INVERT = False    # True als een inverterende schakeling wordt gebruikt
LED_CHANNEL = 0       # Meestal 0, tenzij alternatieve PWM-kanaal
strip_type = ws.SK6812_STRIP_RGBW  # LED-strip type SK6812 RGBW

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN) 

# Initialiseer de LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                     LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

# Moving average filter voor stabiele metingen
window_size = 5  
distance_buffer = np.zeros(window_size)

def measure_distance():
    """ Meet de afstand en past een gemiddelde filter toe voor stabiliteit. """
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.001)  # Minimal stabilization time

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

    # Voer bewegingsgemiddelde filter toe
    global distance_buffer
    distance_buffer = np.roll(distance_buffer, -1)
    distance_buffer[-1] = distance
    filtered_distance = np.mean(distance_buffer)

    return max(5, min(filtered_distance, LED_COUNT * 1.5))  # Afstanden beperken voor stabiliteit

def update_leds(distance):
    """ Directe LED-updates zodat ze altijd de hand volgen. """
    leds_to_light = int(distance / 1.5)  
    print(f"Afstand: {distance:.2f} cm -> LEDs aan: {leds_to_light}")

    for i in range(LED_COUNT):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(255, 255, 0, 0))  # Geel
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))  # LED uit

    strip.show()  

try:
    while True:
        distance = measure_distance()  # Meet real-time afstand
        update_leds(distance)  # Instant LED-update

except KeyboardInterrupt:
    print("Programma gestopt")
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0, 0))  
    strip.show()
    GPIO.cleanup()

except KeyboardInterrupt:
    print("Programma gestopt")
    set_all_leds(Color(0, 0, 0, 0))  # Alle LEDs uitzetten
    GPIO.cleanup()
```

## Samples laten afspelen alsook de LEDs interactief laten meebewegen aan de hand van de ultrasone senor (HC-SR04).

Dit project gebruikt een ultrasone sensor (HC-SR04) om afstanden te meten en op basis daarvan zowel een LED-strip als geluiden te activeren.  
Omdat **pygame** niet als `sudo` kan worden uitgevoerd, hebben we het systeem opgesplitst in twee aparte Python-programma’s die communiceren via een text file.

### Deze werkt met USB en/of met bluetooth
Het probleem ontstaat omdat de 3.5mm AV-jack van de Raspberry Pi 4 beide PWM-kanalen (PWM0 en PWM1) gebruikt voor audio-uitvoer. Tegelijkertijd gebruikt de LED-strip GPIO18 (PWM0), wat een conflict veroorzaakt. Hierdoor stopt het geluid volledig zodra de LED-strip wordt aangestuurd. Het geluid werkt pas weer na een herstart van de Raspberry Pi.

### Uitleg programma's?  
1. **`led_distance_control.py`**:
   - Meet de afstand met de HC-SR04 sensor.
   - Schrijft de gemeten afstand naar een tekstbestand (`distance.txt`).
   - Past de LED-strip aan op basis van de afstand.

2. **`sound_player.py`**:
   - Leest de afstand uit `distance.txt`.
   - Speelt het juiste geluid af afhankelijk van de afstand.

  | Script                  | Moet met `sudo`? | Functionaliteit                                                  | Reden                                                             |
|-------------------------|-----------------|-----------------------------------------------------------------|-------------------------------------------------------------------|
| `led_distance_control.py` | ✅ **Ja**       | Meet de afstand en bestuurt de LED-strip                         | Gebruikt GPIO en bestuurt de LED-strip (vereist rootrechten)      |
| `sound_player.py`       | ❌ **Nee**        | Leest de afstand uit een tekstbestand en speelt het juiste geluid af | `pygame.mixer` werkt niet onder sudo; audio vereist gebruikersrechten |
   
### Programma's
1. **`led_distance_control.py`**
```python
import time
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color, ws
import numpy as np

# Instellingen afstandssensor
TRIG_PIN = 5
ECHO_PIN = 6

# LED-strip instellingen
LED_COUNT = 100
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 50
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
    print(f"Afstand: {distance:.2f} cm -> LEDs aan: {leds_to_light}")

    for i in range(LED_COUNT):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(255, 255, 0, 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def write_distance_to_file(distance):
    with open("distance.txt", "w") as file:
        file.write(str(distance))

try:
    while True:
        distance = measure_distance()
        update_leds(distance)
        write_distance_to_file(distance)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programma gestopt")
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()
    GPIO.cleanup()
```

2. **`sound_player.py`**
```python
import time
import pygame

# Initialiseer pygame voor audio
pygame.mixer.init()

# Laad de audiobestanden
short_sound = pygame.mixer.Sound("sample1.wav")  
medium_sound = pygame.mixer.Sound("sample2.wav")  
long_sound = pygame.mixer.Sound("sample3.wav")    

distance_file = "/home/RPI1/distance.txt"

def read_distance():
    """Leest de afstand uit het tekstbestand en retourneert de waarde."""
    try:
        with open(distance_file, "r") as file:
            return float(file.read().strip())
    except:
        return None  # Retourneer None als er een fout optreedt

def play_sound(distance):
    """Speelt een geluid af op basis van de afstand."""
    if distance < 30:
        short_sound.play()
        print("Speelt sample 1 af")
    elif 30 <= distance < 60:
        medium_sound.play()
        print("Speelt sample 2 af")
    elif distance >= 60:
        long_sound.play()
        print("Speelt sample 3 af")

try:
    while True:
        distance = read_distance()
        if distance is not None:
            play_sound(distance)
        time.sleep(0.5)  # Voorkom overbelasting van het systeem

except KeyboardInterrupt:
    print("Sound player gestopt")
```

### Uitvoering
```bash
sudo python3 led_distance_control.py
```

```bash
python3 sound_player.py
```

- led_distance_control.py moet als sudo draaien, omdat het de GPIO en LED-strip bestuurt.


- sound_player.py mag niet als sudo draaien, omdat pygame anders niet werkt.
```bash
import pygame
import time
import os

# Initialiseer pygame
pygame.mixer.init()

# Zet de juiste pad naar de bestanden
base_path = "/home/RPI2/Sounds/piano/"  # Update het pad naar de nieuwe locatie
short_sound = pygame.mixer.Sound(os.path.join(base_path, "sample1.wav"))
medium_sound = pygame.mixer.Sound(os.path.join(base_path, "sample2.wav"))
long_sound = pygame.mixer.Sound(os.path.join(base_path, "sample3.wav"))

distance_file = "/home/RPI2/distance.txt"

def read_distance():
    """Leest de afstand uit het tekstbestand en retourneert de waarde."""
    try:
        with open(distance_file, "r") as file:
            return float(file.read().strip())
    except:
        return None  # Retourneer None als er een fout optreedt

def play_sound(distance):
    """Speelt een geluid af op basis van de afstand."""
    if distance < 30:
        short_sound.play()
        print("Speelt sample 1 af")
    elif 30 <= distance < 60:
        medium_sound.play()
        print("Speelt sample 2 af")
    elif distance >= 60:
        long_sound.play()
        print("Speelt sample 3 af")

try:
    while True:
        distance = read_distance()
        if distance is not None:
            play_sound(distance)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Sound player gestopt")
```
