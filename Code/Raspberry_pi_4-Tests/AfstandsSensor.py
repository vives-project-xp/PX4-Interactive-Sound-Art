import time
import RPi.GPIO as GPIO

# Configuratie van de ultrasone sensor
TRIG_PIN = 5  # Trigger-pin
ECHO_PIN = 6  # Echo-pin

# GPIO-initialisatie
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

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
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Test gestopt")
    GPIO.cleanup()
