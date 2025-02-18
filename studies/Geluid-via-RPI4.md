# Geluid afspelen op de Raspberry Pi 4

Voor het afspelen van geluid op de Raspberry Pi 4 hebben we de volgende tools gebruikt:

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