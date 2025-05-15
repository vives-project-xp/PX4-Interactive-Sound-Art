In deze README wordt uitgelegd hoe je de **Pi4** moet **opzetten**, hoe je **extra lichteffecten** kunt toevoegen en hoe je **extra geluiden** toevoegt op de Pi zelf. Tot slot wordt uitgelegd hoe je gemakkelijk een **tweede Pi** kunt instellen.


# 1. Pi4 instellen

Gebruik de volgende commando's om de juiste library's te installeren:
```bash
sudo apt update
```
```bash
sudo apt install -y \
  python3-pip python3-dev build-essential \
  libffi-dev libssl-dev \
  python3-rpi.gpio python3-numpy python3-pygame
```
```bash
sudo pip3 install \
  rpi_ws281x \
  flask \
  flask-cors \
  flask-socketio \
  python-socketio \
  requests \
  pygame \
  eventlet
```

Moeite met de rpi_ws281x? Probeer het volgende:
```bash
sudo pip3 install rpi_ws281x --break-systeel-packages
```
Test of het correct is geïnstalleerd: 
```bash
sudo python3 -c "import rpi_ws281x"
```
Nu kun je alle scripts en sounds op de Pi zetten van de github. Zet de scripts onder de map ``/home/RPI2/Documents/`` en **noem ze zoals ze staan op de Github.** Zet dan alle sounds onder de map ``/home/RPI2/Documents/Sounds/`` **Gebruik ook hier de zelfde benaming als op GitHub!!**

Run file:
```bash
sudo python3 /home/RPI2/Documents/main.py
```
```bash
python3 /home/RPI2/Documents/sound_player.py
```

## Auto start van scripts
Als je wilt dat je scripts automatisch starten zodra de Pi aanstaat, kun je dit instellen via systemd.


Maak onderstaande files aan in de map ``/etc/systemd/system/``

``sound_player.service``
```
[Unit]
Description=Sound Player Service
After=led_sensor.service sound.target
Requires=led_sensor.service

[Service]
User=RPI2
Environment=XDG_RUNTIME_DIR=/run/user/1000
Type=simple
WorkingDirectory=/home/RPI2/Documents
ExecStart=/usr/bin/python3 /home/RPI2/Documents/sound_player.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```


``led_sensor.service``
```
[Unit]
Description=Sound-Art Main Service (Flask + LED)
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/RPI2/Documents
ExecStart=sudo python3  /home/RPI2/Documents/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Om de systemd-services te activeren, voer je de volgende commando's uit in de terminal:
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl enable sound_player.service
```
```bash
sudo systemctl enable led_sensor.service
```
```bash
sudo systemctl start sound_player.service
```
```bash
sudo systemctl start led_sensor.service
```
Heb je een probleem met de scripts die niet werken? Dan kun je alle logs zien sinds de laatste boot met onderstaande commando's :
```bash
sudo journalctl -u sound_player.service -b
```
```bash
sudo journalctl -u led_sensor.service -b
```


# 2. Hoe extra lichteffecten toe voegen?
In dit gedeelte leer je hoe je lichteffecten aan je project kunt toevoegen.

## Voeg de code toe op de Pi4
**Stap 1 : maak je effect in de bibliotheek**

Bepaal eerst of je effect een kleur nodig heeft. Bijvoorbeeld, bij het regenboogeffect is het niet nodig om een kleur te kiezen. Voeg vervolgens je code toe in het led_effects.py script. Je kunt bijvoorbeeld beginnen met:

```python
 def UrNewEffect(strip, leds_to_light, hex_color):
    # Your custom code here.
    # - leds_to_light: the number of LEDs that need to be on.
    # - hex_color: the color in hexadecimal (not needed for effects like rainbow).
    # - strip: use strip.setPixelColor(i, Color(0, 0, 0, 0)) to set colors.

```

Vanaf hier kun je je eigen effect implementeren.

**Stap 2 : voeg de code toe aan het main.py bestand**

Importeer je nieuwe effect in je main.py script, samen met de bestaande effecten:
```python
from led_effects import (effect_solid, effect_puls, effect_rainbow, effect_chase, effect_fire, effect_sparkle, IdleEffect , UrNewEffect)
```
Werk vervolgens je ``update_leds()`` functie bij om je effect toe te voegen: 

```python
def update_leds(leds_to_light):
    if current_effect == "solid":
        effect_solid(strip, leds_to_light, current_color)
    elif current_effect == "puls":
        effect_puls(strip, leds_to_light, current_color)
    elif current_effect == "rainbow":
        effect_rainbow(strip, leds_to_light)
    elif current_effect == "chase":
        effect_chase(strip, leds_to_light, current_color)
    elif current_effect == "fire":
        effect_fire(strip, leds_to_light)
    elif current_effect == "sparkle":
        effect_sparkle(strip, leds_to_light, current_color)
    elif current_effect == "UrNewEffect"
        UrNewEffect(strip, leds_to_light, current_color)
    else:
        effect_solid(strip, leds_to_light, current_color)
```


# 3. Hoe extra geluiden toe te voegen?
In dit gedeelte leer je hoe je extra geluiden aan je project kunt toevoegen.

## Voeg de code toe op de Pi4
**Stap 1 : Zet het geluid in de juiste map**

Begin met het plaatsen van je map met geluiden in de map ``home/RPI2/Documents/Sound``. 
![Fysieke_box](../Technische_documentatie/Foto's/Sound_Folder.png)

Je hebt **8** verschillende tonen van je geluid nodig. Deze moeten genoemd worden als  ``niveau 1.mp3``, ``niveau 2.mp3``, ``niveau 3.mp3``, .... ,``niveau 8.mp3``.
**Niveau 1 wordt afgespeeld bij de laagste afstand, en niveau 8 bij de hoogste afstand.**

![Fysieke_box](../Technische_documentatie/Foto's/New_Sound_Folder.png)

**Stap 2 : Voeg je geluid toe in de ``sound_player.py``**
```python
instruments = {
    "gitaar": load_instrument_sounds("gitaar"),
    "drum": load_instrument_sounds("drum"),
    "bass jumpy": load_instrument_sounds("bass jumpy"),
    "bell": load_instrument_sounds("bell"),
    "synth Sci-Fi": load_instrument_sounds("synth Sci-Fi"),
    "synth sharp": load_instrument_sounds("synth sharp"),
    "bassline": load_instrument_sounds("bassline"),
    "UrNewSound": load_instrument_sounds("UrNewSound")    
}
```
 ### Hoe de afstandsinstellingen te wijzigen

 Als je de afstand waarop de geluiden worden afgespeeld wilt wijzigen, kun je dit doen in de ``get_level()`` functie in het main.py bestand.
```python
def get_level(distance):
    if distance < 10:
        return 1
    elif distance < 20:
        return 2
    elif distance < 30:
        return 3
    elif distance < 40:
        return 4
    elif distance < 50:
        return 5
    elif distance < 60:
        return 6
    elif distance < 70:
        return 7
    else:
        return 8     
```

## Meerdere Pi’s instellen

Als je dit project op meerdere Raspberry Pi’s wilt draaien, kun je het handigst één volledig geconfigureerde SD-kaart klonen en op de andere Pi’s gebruiken. Dit doe je in twee stappen met **balenaEtcher**:

1. **SD-kaart uitlezen**  
   – Sluit de bron-SD-kaart aan op je pc en maak er met balenaEtcher een `.img`-bestand van.  
2. **SD-kaart flashen**  
   – Schrijf dat `.img`-bestand naar de doel-SD-kaart en steek die in de volgende Pi.

Ná het klonen moet je in `main.py` twee variabelen per Pi nog aanpassen, zodat elke Pi uniek is en met de website communiceert:

```python
# Regel 62: box-nummer van deze Pi
box_id = "Vul_hier_je_box_nummer_in"

# Regel 213: Tailscale-IP van deze Pi
tailscale_ip = "IP_Van_Je_Pi"
