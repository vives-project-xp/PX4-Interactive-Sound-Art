# miniatuur luidspreker (ongeveer 10W)

- Relatief goedkoop (10 - 15 euro)
- Kan je mooi aan de "doos" monteren 
- PAM8610 of andere module nodig voor aansluiting met de pi (12V voeding aangeraden)
- ![alt text](./fotos/versterkingsmodule.webp)
- LM385 audio amplifier (voorbeeld: https://www.instructables.com/ESP-32-Based-Audio-Player/) 

- **Extra info**: 
  - De PAM8610 biedt 10W vermogen per kanaal (stereo-output).
  - Je kunt de speaker en pi 4 via de 3.5mm audio jack aansturen en de pi 5 GPIO-PWM aansluiten (denk ik).

### Voordelen:
- Flexibel en krachtiger dan USB-speakers.
- Geschikt voor maatwerkprojecten en betere geluidskwaliteit.
- Geen softwarematige drivers nodig.
S
### Nadelen:
- Complexere setup met aparte voeding en mogelijk soldeerwerk.
- Kans op storing bij incorrecte bekabeling of voeding.

---
# gewone usb speaker

- Relatief goedkoop (10 - 25 euro)
- Makkelijker aansluitbaar
- Sommige goedkope speakers werken niet goed zonder extra drivers

### Voordelen:
- Eenvoudig aan te sluiten, geen aparte voeding nodig.
- Wordt direct herkend als een USB-audioapparaat door Raspberry Pi OS.
- Ideaal voor eenvoudige projecten.

### Nadelen:
- Goedkope modellen kunnen problemen geven:
  - Sommige vereisen specifieke drivers die mogelijk niet standaard ondersteund worden.
  - Lagere geluidskwaliteit in vergelijking met custom-oplossingen.
- Geluidsniveau en kwaliteit kunnen tegenvallen.
- Kan problemen geven als meerdere USB-apparaten veel stroom trekken (zonder powered USB-hub).

---

# Voordelen van de Monacor SPM-200X/4 voor een Sound Art Systeem SPRINT 2

## 1. **Breed frequentiebereik voor een rijk geluid**
   - Als een breedband-luidspreker bestrijkt de **SPM-200X/4** een groot deel van het hoorbare spectrum zonder de noodzaak van extra tweeters of subwoofers.
   - Ideaal voor het reproduceren van zowel lage als hoge tonen in een interactieve sound art installatie.

## 2. **Hoge belastbaarheid (60W)**
   - Kan **hoge volumes aan zonder vervorming**, wat handig is voor een dynamische en meeslepende ervaring.
   - Werkt goed met de **TPA3116D2 versterker**, die een vergelijkbaar vermogen aankan.

## 3. **Lage impedantie (4Ω)**
   - Perfect geschikt voor de **TPA3116D2 versterkermodule**, die is ontworpen om efficiënt met 4Ω belastingen te werken.
   - Zorgt voor een betere stroomtoevoer en geluidskwaliteit.

## 4. **Efficiënte koppeling met de TPA3116D2**
   - De **TPA3116D2 klasse-D versterker** is efficiënt en genereert weinig warmte.
   - Door de **lage THD (Total Harmonic Distortion)** blijft het geluid helder, wat belangrijk is voor sound art waarbij nuances in geluid cruciaal zijn.


## 6. **Compatibiliteit met Raspberry Pi 4**
   - De Raspberry Pi 4 kan de **TPA3116D2 aansturen via I2S of via een externe USB-DAC**, wat zorgt voor een hoge kwaliteit digitale audio-uitvoer.
   - Geschikt voor interactieve toepassingen waarbij de audio real-time gemanipuleerd wordt.

## 7. **Goede prijs-kwaliteitverhouding**
   - In vergelijking met hi-fi luidsprekers biedt de Monacor SPM-200X/4 een uitstekende balans tussen **prijs en prestaties**.
   - Geschikt voor een budgetvriendelijk project zonder in te leveren op geluidskwaliteit.
