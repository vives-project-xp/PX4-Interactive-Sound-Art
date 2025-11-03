#!/usr/bin/env python3
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
    We verwachten bestanden niveau 1.mp3, niveau 2.mp3, ... niveau 8.mp3.
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
    "Gitaar": load_instrument_sounds("gitaar"),
    "Drum": load_instrument_sounds("drum"),
    "Bass jumpy": load_instrument_sounds("bass jumpy"),
    "Bell": load_instrument_sounds("bell"),
    "Synth Sci-Fi": load_instrument_sounds("synth Sci-Fi"),
    "Synth sharp": load_instrument_sounds("synth sharp"),
    "Bassline": load_instrument_sounds("bassline")
}

default_instrument = instruments.get("Gitaar")  # Als het ontvangen instrument niet herkend wordt

# Pad voor statusbestand waarin afstand en instrument worden opgeslagen
status_file = "/home/RPI2/Documents/txtFile/status.json"

def read_status():
    """Leest de status (instrument, sound_level, sound_stop en volume) uit het JSON-bestand.
    Zet volume (0-100) om naar 0.0-1.0."""
    try:
        with open(status_file, "r") as file:
            status = json.load(file)
            raw_vol = status.get("volume", 100)
            vol = max(0, min(raw_vol, 100)) / 100.0
            return status.get("instrument"), status.get("sound_level"), status.get("sound_stop"), vol
    except Exception as e:
        print("Error reading status file:", e)
        return None, None, None, 1.0


def play_sound(sound_level, instrument, sound_stop, volume):
    """
    Speelt een geluid af op basis van het sound_level en instrument.
    Er wordt gekeken naar het instrument dat in het statusbestand staat en de bijbehorende geluiden worden gebruikt.
    Bij sound_stop False speelt het geluid met het meegegeven volume.
    """
    sounds = instruments.get(instrument, default_instrument)
    if sounds is None:
        print(f"Geen geluiden gevonden voor instrument: {instrument}")
        return

    if sound_stop:
        pygame.mixer.stop()
        print("Sound Off")
        return
    
    sound: pygame.mixer.Sound = sounds.get("niv"+str(sound_level))
    if sound:
        sound.set_volume(volume)
        sound.play()
        print(f"Speelt {instrument} sample niveau {sound_level} af met volume {volume*100:.0f}%")
    else:
        print("Ongeldig geluidsniveau")
        

try:
    while True:
        instrument, sound_level, sound_stop, volume = read_status()
        print(sound_level)
        if sound_level is not None and instrument is not None:
            play_sound(sound_level, instrument, sound_stop, volume)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Programma gestopt")