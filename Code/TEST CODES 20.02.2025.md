# WERKT !!!!!!!!!!!!!Ultrasone sensor (hc-sr04) met RPI4

### How it works

The program sets up the TRIG pin as an output and the ECHO pin as an input.
The get_distance function sends a pulse on the TRIG pin and measures the time it takes for the pulse to bounce back and be received on the ECHO pin.
The distance is calculated using the formula distance = pulse_duration * 17150, where pulse_duration is the time it took for the pulse to bounce back.
The program prints the distance every 0.1 seconds.

### Notes

Make sure to connect the HC-SR04 sensor to the Raspberry Pi correctly:
HC-SR04  | Raspberry Pi 4
---------|---------
VCC      | 5V (pin 2)
GND      | GND (pin 6)
TRIG     | GPIO 23 
ECHO     | GPIO 24 

You may need to adjust the TRIG_PIN and ECHO_PIN variables to match your specific setup.
This program uses the BCM pin numbering scheme. If you're using a different scheme, you'll need to adjust the pin numbers accordingly.
You can adjust the time.sleep(0.1) line to change the update rate of the distance readings.

```python
import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the HC-SR04 sensor
TRIG_PIN = 23
ECHO_PIN = 24

# Set up the TRIG pin as an output and the ECHO pin as an input
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Set the TRIG pin high for 10 microseconds to send a pulse
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for the ECHO pin to go high
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()

    # Wait for the ECHO pin to go low
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

    # Calculate the distance
    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 17150

    return distance

try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
```
 
#  WEKRT !!!!!!!!!!!!!! Samples afspelen tussen bepaalde waarden.

```python
import pygame
import time
import random  # Simuleert een variabele waarde (vervang dit met een sensor)

# Initialiseer pygame mixer
pygame.mixer.init()

# Laad de geluidssamples
sample1 = pygame.mixer.Sound("sample1.wav")
sample2 = pygame.mixer.Sound("sample2.wav")
sample3 = pygame.mixer.Sound("sample3.wav")

def get_waarde():
    """Simuleert een veranderende waarde, vervang dit met echte sensordata."""
    return random.randint(0, 100)  # Simuleert een waarde tussen 0 en 100

try:
    while True:
        waarde = get_waarde()
        print(f"Waarde: {waarde}")

        if 0 <= waarde < 30:
            sample1.play()
            print("Speelt sample 1 af")
        elif 30 <= waarde < 60:
            sample2.play()
            print("Speelt sample 2 af")
        elif waarde >= 60:
            sample3.play()
            print("Speelt sample 3 af")

        time.sleep(1)  # Wacht 1 seconde voor de volgende meting

except KeyboardInterrupt:
    print("Programma gestopt")

```

```bash
python3 play_samples.py
```

# WERKT ( rare interval) Samples afspelen aan de hand van de ultrasone sensor (hc-sr04)
- Sample 1 speelt af als de afstand kleiner is dan 30 cm.
- Sample 2 speelt af als de afstand tussen 30 cm en 60 cm ligt.
- Sample 3 speelt af als de afstand groter is dan 60 cm.

De HC-SR04 ultrasone sensor werkt op 5V, maar de GPIO-pinnen van de Raspberry Pi 4 werken op 3.3V. Daarom heb je een logische niveauschakelaar (level shifter) of een spanningsdeler nodig voor de ECHO-pin, anders kan dit je Raspberry Pi beschadigen!

Benodigde onderdelen:
✅ HC-SR04 ultrasone sensor
✅ Raspberry Pi 4
✅ 1x 1kΩ weerstand
✅ 1x 2kΩ weerstand (voor de spanningsdeler op de ECHO-pin)
✅ Jumper wires

| **HC-SR04 Pin** | **Raspberry Pi 4 Pin** | **Opmerking** |
|---------------|------------------|------------|
| **VCC**       | **5V (Pin 2 of 4)** | Voeding voor de sensor |
| **GND**       | **GND (Pin 6, 9, 14, etc.)** | Aarde |
| **TRIG**      | **GPIO 5 (Pin 29)** | Stuur een puls om meting te starten |
| **ECHO**      | **GPIO 6 (Pin 31) via spanningsdeler** | Meet de afstand, verlagen naar 3.3V! |

Daarom gebruiken we een spanningsdeler met een 1kΩ en een 2kΩ weerstand:

🔽 Zo verbind je het:

- ECHO van HC-SR04 → 2kΩ weerstand → GPIO 6 (Pin 31)
- ECHO van HC-SR04 → 1kΩ weerstand → GND van Raspberry Pi

Waarom werkt dit?

De spanningsdeler verlaagt 5V naar ~3.3V, zodat het veilig is voor de Raspberry Pi.
Wat als je een bi-directionele level shifter hebt?
Als je een bi-directionele 5V naar 3.3V level shifter hebt (zoals de TXB0108), kun je die gebruiken in plaats van een spanningsdeler.

VCC HC-SR04 → 5V van de Raspberry Pi
ECHO via level shifter naar GPIO 6
TRIG direct naar GPIO 5
Software Setup (Zorg dat alles werkt!)
Voordat je het script draait, installeer de juiste pakketten:

```bash
sudo apt-get install python3-pygame
pip install RPi.GPIO
```

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
sample1 = pygame.mixer.Sound("sample1.wav")
sample2 = pygame.mixer.Sound("sample2.wav")
sample3 = pygame.mixer.Sound("sample3.wav")

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

# Ultrasone senor met LEDs (sam test)

```python
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
    
```

## Belangrijke punten voor het gebruik van dit programma
Dit programma gebruikt een Raspberry Pi 4, een HC-SR04 ultrasone sensor en een SK6812 RGBW LED-strip. Het meet de afstand met de ultrasone sensor en laat een overeenkomstig aantal LEDs oplichten. Als de sensor 5 seconden geen object detecteert binnen 177 cm, schakelt de LED-strip uit.

### Benodigde hardware:
- Raspberry Pi 4
- HC-SR04 ultrasone sensor
- SK6812 RGBW LED-strip (100 LEDs)
- 5V voeding voor de LED-strip
- Weerstanden & spanningsdeler (voor de HC-SR04 ECHO-pin)
- Verbindingen met de Raspberry Pi 4:
- HC-SR04 Ultrasone Sensor

### Verbindingen met de Raspberry Pi 4:
HC-SR04 Ultrasone Sensor
| **HC-SR04 Pin** | **Raspberry Pi 4 Pin**       | **Opmerking**                              |
|---------------|-------------------------|----------------------------------|
| **VCC**       | **5V (Pin 2 of 4)**      | Voeding voor de sensor          |
| **GND**       | **GND (Pin 6, 9, 14, etc.)** | Aarde                           |
| **TRIG**      | **GPIO 5 (Pin 29)**      | Stuur een puls om meting te starten |
| **ECHO**      | **GPIO 6 (Pin 31) via spanningsdeler** | Meet afstand, verlagen naar 3.3V! |

### LED-strip -> Raspberry Pi 4
| **LED-strip Pin** | **Raspberry Pi 4 Pin**       | **Opmerking**                      |
|------------------|-------------------------|--------------------------------|
| **VCC (5V)**    | **Externe 5V voeding**   | Niet direct op Raspberry Pi!  |
| **GND**         | **GND (Raspberry Pi en voeding delen GND)** | Gemeenschappelijke aarde |
| **DIN (Data In)** | **GPIO 18 (Pin 12)**    | Moet PWM ondersteunen!        |
| **GND (extra)**  | **GND**                 | Extra stabiliteit voor data   |

- De LED-strip trekt te veel stroom voor de Raspberry Pi. Gebruik een externe 5V voeding.
- GND van de LED-strip, de voeding en de Raspberry Pi moeten verbonden zijn!
- GPIO 18 moet worden gebruikt, omdat het PWM-output ondersteunt.



# ZELFDE ALS 2 HIERBOEVN WERKT !!!!!!!!!!!!!!Audio-samples afspelen op basis van afstandsmetingen van de HC-SR04 ultrasone sensor
 
```python
import time
import RPi.GPIO as GPIO
import pygame

# GPIO-configuratie voor de HC-SR04
TRIG_PIN = 5  # GPIO 5 - Trigger
ECHO_PIN = 6  # GPIO 6 - Echo

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer pygame voor audio
pygame.mixer.init()

# Laad de audiobestanden
short_sound = pygame.mixer.Sound("short_sound.wav")  
medium_sound = pygame.mixer.Sound("medium_sound.wav")  
long_sound = pygame.mixer.Sound("long_sound.wav")    

def meet_afstand():
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
    afstand = (elapsed_time * 34300) / 2  # Omrekenen naar cm
    return afstand

try:
    while True:
        afstand = meet_afstand()
        print(f"Afstand: {afstand:.2f} cm")

        # Geluid afspelen op basis van afstandswaarde
        if afstand < 20:
            short_sound.play()  # Speel korte sound af bij kleine afstand
        elif 20 <= afstand < 50:
            medium_sound.play()  # Speel een ander geluid af bij middellange afstand
        elif afstand >= 50:
            long_sound.play()  # Speel lang geluid bij grote afstand
        
        time.sleep(1)  # Kleine pauze om herhaalde metingen te vermijden

except KeyboardInterrupt:
    print("Programma gestopt")
    GPIO.cleanup()
```
| **HC-SR04 Pin** | **Raspberry Pi 4 Pin**       | **Opmerking**                              |
|---------------|-------------------------|----------------------------------|
| **VCC**       | **5V (Pin 2 of 4)**      | Voeding voor de sensor          |
| **GND**       | **GND (Pin 6, 9, 14, etc.)** | Aarde                           |
| **TRIG**      | **GPIO 5 (Pin 29)**      | Stuur een puls om meting te starten |
| **ECHO**      | **GPIO 6 (Pin 31) via spanningsdeler** | Meet afstand, verlagen naar 3.3V! |

# Alles samen

### Uitleg van het programma:
- De sensor meet de afstand tot een object en stuurt deze informatie naar de Raspberry Pi.
- De afstand wordt gebruikt om te bepalen welk geluidssample moet worden afgespeeld en hoeveel LEDs er moeten oplichten.

### Geluidssamples:
- Drie geluidssamples worden geladen (sample1.wav, sample2.wav, sample3.wav).
- Afhankelijk van de gemeten afstand wordt een van deze samples afgespeeld:
- sample1.wav voor afstanden kleiner dan 30 cm.
- sample2.wav voor afstanden tussen 30 cm en 60 cm.
- sample3.wav voor afstanden groter dan of gelijk aan 60 cm.

### LED-strip:
- De LED-strip wordt aangestuurd op basis van de gemeten afstand.
- Het aantal LEDs dat oplicht is evenredig met de afstand (1.5 cm per LED).
- De LEDs die oplichten zijn geel (Color(255, 255, 0, 0)), terwijl de rest uit blijft.

### Time-out:
- Als de sensor gedurende 5 seconden geen object detecteert binnen 177 cm, worden alle LEDs uitgezet.

### GPIO-instellingen:
- De GPIO-pinnen zijn correct ingesteld voor de HC-SR04 sensor en de LED-strip.
- De ECHO-pin van de HC-SR04 is verbonden via een spanningsdeler om de spanning te verlagen naar 3.3V.

## Benodigde hardware:
- Raspberry Pi 4
- HC-SR04 ultrasone sensor
- SK6812 RGBW LED-strip (100 LEDs)
- 5V voeding voor de LED-strip
- Weerstanden & spanningsdeler (voor de HC-SR04 ECHO-pin)

## Verbindingsdraden

### Verbindingen:
#### HC-SR04:
- VCC -> 5V (Pin 2 of 4)
- GND -> GND (Pin 6, 9, 14, etc.)
- TRIG -> GPIO 5 (Pin 29)
- ECHO -> GPIO 6 (Pin 31) via spanningsdeler

#### LED-strip:
- VCC (5V) -> Externe 5V voeding
- GND -> GND (Raspberry Pi en voeding delen GND)
- DIN (Data In) -> GPIO 18 (Pin 12)
- GND (extra) -> GND

## Installatie:
Zorg ervoor dat je de benodigde bibliotheken hebt geïnstalleerd:
```bash
sudo apt-get install python3-pygame
pip install rpi_ws281x RPi.GPIO
```

uitvoeren
```bash
python3 ultrasone_led_audio.py
```

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
short_sound = pygame.mixer.Sound("sample1.wav")  
medium_sound = pygame.mixer.Sound("sample2.wav")  
long_sound = pygame.mixer.Sound("sample3.wav")    

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

# NIEUW
```python
import time
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color, ws

# LED-strip configuratie
LED_COUNT = 100       # Aantal LEDs
LED_PIN = 18          # GPIO voor LED-data
LED_FREQ_HZ = 800000  # Frequentie (standaard 800kHz)
LED_DMA = 10          # DMA-kanaal
LED_BRIGHTNESS = 100  # Helderheid (0-255)
LED_INVERT = False    # Inverteren (standaard False)
LED_CHANNEL = 0       # PWM-kanaal
STRIP_TYPE = ws.SK6812_STRIP_RGBW  # LED-strip type

# Afstandssensor configuratie
TRIG_PIN = 5  # Trigger op GPIO 5
ECHO_PIN = 6  # Echo op GPIO 6
CM_PER_LED = 1.5  # Hoeveel cm per LED

TIMEOUT_LIMIT = 20  # Hoeveel metingen tot LED-strip uitgaat (5 sec)

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                   LED_BRIGHTNESS, LED_CHANNEL, strip_type=STRIP_TYPE)
strip.begin()

def set_all_leds(color):
    """Zet alle LEDs op dezelfde kleur."""
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
    strip.show()

def measure_distance():
    """Meet afstand met de HC-SR04 sensor."""
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  # Wachten voor stabiliteit

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    # Wachten op signaal
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Bereken afstand
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Omrekenen naar cm
    return distance

try:
    timeout_counter = 0  # Timer voor uitschakelen LED-strip

    while True:
        distance = measure_distance()
        print(f"Afstand: {distance:.2f} cm")

        leds_to_light = int(distance / CM_PER_LED)
        print(f"Aantal LEDs aan: {leds_to_light}")

        # Controleer of object binnen 177 cm is
        if distance > 177:
            timeout_counter += 1
        else:
            timeout_counter = 0

        if timeout_counter < TIMEOUT_LIMIT:
            for i in range(LED_COUNT):
                if i < leds_to_light:
                    strip.setPixelColor(i, Color(255, 0, 255, 0))  # Magenta kleur
                else:
                    strip.setPixelColor(i, Color(0, 0, 0, 0))  # LED uit
        else:
            set_all_leds(Color(0, 0, 0, 0))  # LED-strip uit

        strip.show()
        time.sleep(0.25)  # Snelheid aanpassen

except KeyboardInterrupt:
    print("Programma gestopt")
    set_all_leds(Color(0, 0, 0, 0))
    GPIO.cleanup()
```

1. ModuleNotFoundError: No module named 'rpi_ws281x'
```bash
pip3 install --break-system-packages rpi-ws281x

```

2. RuntimeError: ws2811_init failed with code -5
```bash
sudo systemctl stop pigpiod
sudo systemctl disable pigpiod
```

3.🚀 Bonus: Kleur aanpassen
```bash
strip.setPixelColor(i, Color(R, G, B, W))
```
Can't open /dev/mem: Permission denied
Traceback (most recent call last):
  File "/home/RPI1/Downloads/test sensor", line 30, in <module>
    strip.begin()
  File "/home/RPI1/.local/lib/python3.11/site-packages/rpi_ws281x/rpi_ws281x.py", line 143, in begin
    raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, str_resp))
RuntimeError: ws2811_init failed with code -5 (mmap() failed)

- sudo systemctl stop pigpiod
- sudo systemctl disable pigpiod
- sudo reboot

- sudo usermod -a -G gpio,i2c $(whoami)
- sudo reboot

- sudo raspi-config

- error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.

```python
import time
import RPi.GPIO as GPIO
import pygame
from rpi_ws281x import PixelStrip, Color, ws
import numpy as np  # For moving average filter

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

# LED-strip type (SK6812 RGBW)
strip_type = ws.SK6812_STRIP_RGBW

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer pygame voor audio
pygame.mixer.init()

# Laad de audiobestanden
short_sound = pygame.mixer.Sound("sample1.wav")  
medium_sound = pygame.mixer.Sound("sample2.wav")  
long_sound = pygame.mixer.Sound("sample3.wav")    

# Initialiseer de LED-strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                     LED_BRIGHTNESS, LED_CHANNEL, strip_type=strip_type)
strip.begin()

# Moving average filter for smoothing distance readings
window_size = 5  # Number of readings to average
distance_buffer = np.zeros(window_size)

def measure_distance():
    """ Meet de afstand met de HC-SR04 en retourneert een gefilterde waarde in cm. """
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

    # Store distance in buffer and apply moving average filter
    global distance_buffer
    distance_buffer = np.roll(distance_buffer, -1)
    distance_buffer[-1] = distance
    filtered_distance = np.mean(distance_buffer)

    return max(5, min(filtered_distance, LED_COUNT * 1.5))  # Limit values to avoid errors

def update_leds(distance):
    """ Direct update LEDs to match hand level without delay. """
    leds_to_light = int(distance / 1.5)  # 1.5 cm per LED
    print(f"Afstand: {distance:.2f} cm -> LEDs aan: {leds_to_light}")

    for i in range(LED_COUNT):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(255, 255, 0, 0))  # Geel
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))  # LED uit

    strip.show()  # Directe update zonder vertraging

try:
    while True:
        distance = measure_distance()  # Real-time distance measurement
        update_leds(distance)  # Immediate LED response

except KeyboardInterrupt:
    print("Programma gestopt")
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0, 0))  # Alle LEDs uitzetten
    strip.show()
    GPIO.cleanup()
```

```python
import time
import RPi.GPIO as GPIO
import pygame
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

# Initialiseer pygame voor audio
pygame.mixer.init()

# Laad de audiobestanden
short_sound = pygame.mixer.Sound("sample1.wav")  
medium_sound = pygame.mixer.Sound("sample2.wav")  
long_sound = pygame.mixer.Sound("sample3.wav")    

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

def play_sound(distance):
    """ Speelt een bepaald geluid af op basis van de afstand. """
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
        distance = measure_distance()  # Meet real-time afstand
        update_leds(distance)  # Instant LED-update
        play_sound(distance)  # Speelt geluid af zonder vertraging

except KeyboardInterrupt:
    print("Programma gestopt")
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0, 0))  
    strip.show()
    GPIO.cleanup()


```
