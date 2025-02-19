# Geluid afspelen op de Raspberry Pi 4

## Verbinden met de Raspberry Pi via SSH (Remote connection)

We hebben op afstand verbinding gemaakt met de Raspberry Pi 4 via SSH met het volgende commando:  

```bash
ssh pi@<Raspberry_Pi_IP>
```
Zo kunnen we vanaf onze eigen PC snel en efficiënt taken uitvoeren.

## Voor het afspelen van geluid op de Raspberry Pi 4 hebben we de volgende tools gebruikt:

- **Audio-uitvoer**: We hebben de juiste audio-uitgang (HDMI of 3,5 mm jack) ingesteld via `raspi-config`.
- **Software**: We hebben `mpg123` voor MP3-bestanden en `alsa-utils` voor WAV-bestanden geïnstalleerd.
- **Python**: We gebruikten de `pygame` bibliotheek om geluid af te spelen via een Python-script.

## Stappen:

1. Installeer de benodigde software:
    ```bash
    sudo apt-get install mpg123 alsa-utils python3-pygame
    ```

2. Gebruik een Python-script om geluid af te spelen die we hebben gemaakt en getest via thonny die al op de RPI4 stond:
    ```python
    import pygame

    pygame.mixer.init()
    pygame.mixer.music.load("pad/naar/bestand.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    ```

3. Voer het script uit (wanneer in command promt wordt getest):
    ```bash
    python3 play_audio.py 
    ```

Met deze stappen hebben we ons eerste geluid afspeelt via onze Raspberry Pi 4. 

## Code die word getest op 20/02/2025

Code die het mogelijk maakt om verschillende geluiden aftespelen aan de hand van wat de ultrasone sensor meet
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
