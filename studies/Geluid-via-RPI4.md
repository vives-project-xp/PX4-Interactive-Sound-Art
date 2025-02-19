# Geluid afspelen en sensor-integratie op de Raspberry Pi 4  

## Inleiding  
In dit project hebben we een Raspberry Pi 4 gebruikt om geluid af te spelen en te reageren op metingen van een ultrasone sensor. We hebben audio-uitvoer ingesteld, software geïnstalleerd en een Python-script geschreven om geluid te laten afspelen op basis van afstandsmetingen.  

## Verbinden met de Raspberry Pi via SSH  
We hebben de Raspberry Pi 4 op afstand benaderd (remote connection) met:  

```bash
ssh username@<hostname>
```
Zo kunnen we vanaf onze eigen PC snel en efficiënt taken uitvoeren.

## Benodigde hardware
- Raspberry Pi 4
- Ultrasone afstandssensor (HC-SR04)
- Speakers of hoofdtelefoon
- Jumper wires

## Software-installatie
Om audio en sensormetingen te gebruiken, installeerden we:
```bash
sudo apt-get install mpg123 alsa-utils python3-pygame
```
Daarnaast moeten `RPi.GPIO` en `pygame` correct werken binnen Python.

## Eerste geluidstest
We hebben getest of de Raspberry Pi 4 audio kon afspelen met dit Python-script in Thonny:
```python
import pygame

pygame.mixer.init()
pygame.mixer.music.load("pad/naar/bestand.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
```
Uitvoering via de terminal:
```bash
python3 play_audio.py
```


## Geluid afspelen op basis van afstandsmetingen

Dit script meet afstand met een ultrasone sensor en speelt een geluid af afhankelijk van de afstand:
 ```python
import time
import RPi.GPIO as GPIO
import pygame  # Voor het afspelen van geluid

# Configuratie van de ultrasone sensor
TRIG_PIN = 5  # Trigger-pin
ECHO_PIN = 6  # Echo-pin

# GPIO-initialisatie
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialiseer pygame voor geluid
pygame.mixer.init()

# Laad geluiden in pygame
short_sound = pygame.mixer.Sound("short_sound.wav")  # Vervang dit met je geluidsbestand
long_sound = pygame.mixer.Sound("long_sound.wav")    # Vervang dit met je geluidsbestand

def meet_afstand():
    """Meet de afstand met de ultrasone sensor en retourneert deze in cm."""
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  # Stabiliseer de sensor

    # Stuur een 10µs trigger-puls
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    # Wacht tot de echo-pin hoog wordt
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Wacht tot de echo-pin laag wordt
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Bereken de verstreken tijd en de afstand
    elapsed_time = stop_time - start_time
    afstand = (elapsed_time * 34300) / 2  # Snelheid van geluid = 34300 cm/s
    return afstand

try:
    while True:
        afstand = meet_afstand()
        print(f"Afstand: {afstand:.2f} cm")

        # Geluid afspelen op basis van afstand
        if afstand < 30:
            short_sound.play()  # Kort geluid als afstand kleiner dan 30 cm
        elif afstand >= 30 and afstand <= 100:
            long_sound.play()   # Lang geluid als afstand tussen 30 en 100 cm

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Test gestopt")
    GPIO.cleanup()
 ```
