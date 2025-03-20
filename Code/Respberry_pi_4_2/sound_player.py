import time
import json
import pygame
import os

# Initialiseer pygame voor audio
pygame.mixer.init()

# Basis pad voor de geluiden
SOUNDS_BASE_PATH = "/home/RPI2/Documents/Sounds"

def load_instrument_sounds(instrument_name):
    """
    Laadt drie geluiden voor het gegeven instrument uit de bijbehorende map.
    We verwachten bestanden A.mp3, B.mp3 en C.mp3.
    """
    instrument_path = os.path.join(SOUNDS_BASE_PATH, instrument_name)
    try:
        sounds = {
            "short": pygame.mixer.Sound(os.path.join(instrument_path, "A.mp3")),
            "medium": pygame.mixer.Sound(os.path.join(instrument_path, "B.mp3")),
            "long": pygame.mixer.Sound(os.path.join(instrument_path, "C.mp3"))
        }
        return sounds
    except Exception as e:
        print(f"Fout bij laden van geluiden voor {instrument_name}: {e}")
        return None

# Laad de geluiden voor de instrumenten
instruments = {
    "guitar": load_instrument_sounds("guitar"),
    "piano": load_instrument_sounds("piano"),
    # Voeg hier extra instrumenten toe, bijvoorbeeld:
    # "synth": load_instrument_sounds("synth")
}

# Indien het ontvangen instrument niet herkend wordt, gebruik een standaard instrument.
default_instrument = instruments.get("guitar")  # Of kies een ander standaard instrument

# Pad voor statusbestand waarin afstand en instrument worden opgeslagen
status_file = "/home/RPI2/Documents/txtFile/status.json"

def read_status():
    """Leest de status (afstand en instrument) uit het JSON-bestand en retourneert de waarden."""
    try:
        with open(status_file, "r") as file:
            status = json.load(file)
            return status.get("distance"), status.get("instrument")
    except Exception as e:
        print("Error reading status file:", e)
        return None, None

def play_sound(distance, instrument):
    """
    Speelt een geluid af op basis van de afstand.
    Er wordt gekeken naar het instrument dat in het statusbestand staat en
    de bijbehorende geluiden worden gebruikt.
    """
    sounds = instruments.get(instrument, default_instrument)
    if sounds is None:
        print(f"Geen geluiden gevonden voor instrument: {instrument}")
        return

    if distance < 30:
        sounds["short"].play()
        print(f"Speelt {instrument} sample short af (afstand < 30)")
    elif 30 <= distance < 60:
        sounds["medium"].play()
        print(f"Speelt {instrument} sample medium af (afstand 30-60)")
    elif distance >= 60:
        sounds["long"].play()
        print(f"Speelt {instrument} sample long af (afstand >= 60)")

try:
    while True:
        distance, instrument = read_status()
        if distance is not None and instrument is not None:
            play_sound(distance, instrument)
        time.sleep(0.5)  # Voorkom overbelasting van het systeem
except KeyboardInterrupt: