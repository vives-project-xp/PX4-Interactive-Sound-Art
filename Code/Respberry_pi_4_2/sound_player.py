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
    Laadt 8 geluiden voor het gegeven instrument uit de bijbehorende map.
    We verwachten bestanden niveau 1.mp3 , niveau 2.mp3 , niveau 3.mp3 .... niveau 8.mp3
    """
    instrument_path = os.path.join(SOUNDS_BASE_PATH, instrument_name)
    try:
        sounds = {
            "niv1": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 1.mp3")),
            "niv2": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 2.mp3")),
            "niv3": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 3.mp3")),
            "niv4": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 4.mp3")),
            "niv5": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 5.mp3")),
            "niv6": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 6.mp3")),
            "niv7": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 7.mp3")),
            "niv8": pygame.mixer.Sound(os.path.join(instrument_path, "niveau 8.mp3"))
        }
        return sounds
    except Exception as e:
        print(f"Fout bij laden van geluiden voor {instrument_name}: {e}")
        return None

# Laad de geluiden voor de instrumenten
instruments = {
    "gitaar": load_instrument_sounds("gitaar"),
    "drum": load_instrument_sounds("drum"),
    "bass jumpy": load_instrument_sounds("bass jumpy"),
    "bell": load_instrument_sounds("bell"),
    "synth Sci-Fi": load_instrument_sounds("synth Sci-Fi"),
    "synth sharp": load_instrument_sounds("synth sharp"),
    "bassline": load_instrument_sounds("bassline")
}

default_instrument = instruments.get("gitaar")  #als het ontvangen instrument niet herkent word

# Pad voor statusbestand waarin afstand en instrument worden opgeslagen
status_file = "/home/RPI2/Documents/txtFile/status.json"

def read_status():
    """Leest de status (afstand en instrument) uit het JSON-bestand en retourneert de waarden."""
    try:
        with open(status_file, "r") as file:
            status = json.load(file)
            return status.get("instrument"), status.get("sound_level")
    except Exception as e:
        print("Error reading status file:", e)
        return None, None

def play_sound(sound_level, instrument):
    """
    Speelt een geluid af op basis van de afstand.
    Er wordt gekeken naar het instrument dat in het statusbestand staat en
    de bijbehorende geluiden worden gebruikt.
    """
    sounds = instruments.get(instrument, default_instrument)
    if sounds is None:
        print(f"Geen geluiden gevonden voor instrument: {instrument}")
        return

    match sound_level:
        case 1:
            sounds["niv1"].play()
            print(f"Speelt {instrument} sample niveau 1 af (afstand < 10)")
        case 2:
            sounds["niv2"].play()
            print(f"Speelt {instrument} sample niveau 2 af (afstand 10-20)")
        case 3:
            sounds["niv3"].play()
            print(f"Speelt {instrument} sample niveau 3 af (afstand 20-30)")
        case 4:
            sounds["niv4"].play()
            print(f"Speelt {instrument} sample niveau 4 af (afstand 30-40)")
        case 5:
            sounds["niv5"].play()
            print(f"Speelt {instrument} sample niveau 5 af (afstand 40-50)")
        case 6:
            sounds["niv6"].play()
            print(f"Speelt {instrument} sample niveau 6 af (afstand 50-60)")
        case 7:
            sounds["niv7"].play()
            print(f"Speelt {instrument} sample niveau 7 af (afstand 60-70)")
        case 8:
            sounds["niv8"].play()
            print(f"Speelt {instrument} sample niveau 8 af (afstand >= 70)")
        case _:
            print("Ongeldig geluidsniveau")
try:
    while True:
        instrument, sound_level = read_status()
        if sound_level is not None and instrument is not None:
            play_sound(sound_level, instrument)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Programma gestopt")