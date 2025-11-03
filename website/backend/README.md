# Backend Documentatie

## Inhoud

1. [Feature's](#features)
2. [Installatie en Starten](#installatie-en-starten)
3. [Websocket Events](#websocket-events)
4. [In Memory State](#in-memory-state)
5. [Heartbeat en cleanup](#heartbeat-en-cleanup)

## Features

- **Socket IO**: zorgt voor real time communicatie
- **In Memory opslag**: slaat verbonden apparaten op en dee laatste command's
- **Rooms**: frontend en rpi worden in rooms gestoken zodat aparte events mogelijk zijn.
- **Heartbeat**: zorgt ervoor dat devices automatisch verwijderd worden als ze inactief zijn.

## Installatie en Starten

### Handmatig

1. **Repo clonen**

In de folder waar je het project wilt clone de de [repo](https://github.com/vives-project-xp/PX4-Interactive-Sound-Art). Als dit gebeurt is ga je naar de map van de backend.

```
git clone https://github.com/vives-project-xp/PX4-Interactive-Sound-Art

cd .\PX4-Interactive-Sound-Art\website\backend\
```

2. **Dependencies installeren**

Om alle dependencies te kunnen installeren heb je eerst [node.js](https://nodejs.org/en/download) nodig. Dit kan je online makkelijk downloaden. Als dit geïnstalleerd is doe je het volgende. En zal alles geïnstalleerd worden.

```
npm install
```

3. **Server starten**
Nu is alles klaar en kan je de server aanpassen en starten. Door het volgende command kan je de server opstarten.

```
npm run start
```

Bij het succesvol starten van de server krijg je in de terminal een melding. Dit zegt dat de backend luisterd op dat adres.

### Docker

Docker is geïmplementeerd dus zo kan je het ook makkelijk runnen. Dit kan door het volgende te doen in de root folder van website.

```
docker compuse up --build
```

## Websocket Events

- **register**  
  - *Frontend*: `{ client: "frontend" }`  
  - *Raspberry Pi*: `{ boxId, ip }`  
  Registreert een client. Frontends komen in de "frontends" room, Pi's krijgen een eigen room (`pi-{boxId}`) en worden toegevoegd aan de device-lijst.

- **devices-list**  
  - Wordt naar elke nieuwe client gestuurd met een lijst van alle actieve boxen:  
    `[ { boxId, ip }, ... ]`

- **device-connected**  
  - Wordt naar alle frontends gestuurd als een nieuwe Pi zich registreert:  
    `{ boxId, ip }`

- **device-disconnected**  
  - Wordt naar alle frontends gestuurd als een Pi offline gaat:  
    `{ boxId }`

- **update-settings**  
  - *Frontend*: `{ boxId, settings }`  
  Stuurt nieuwe instellingen (kleur, effect, instrument, volume, ...) naar een specifieke box.  
  De backend bewaart deze in memory en stuurt ze door naar de juiste Pi én alle frontends.

- **command**  
  - Wordt naar een Pi gestuurd als er nieuwe instellingen zijn, en naar alle frontends voor UI-updates:  
    `{ boxId, isOn, color, effect, instrument, volume, ... }`

- **heartbeat**  
  - *Pi*: `{ boxId }`  
  Houdt de Pi actief in de backend. Als er te lang geen heartbeat komt, wordt de box als offline beschouwd.

## In Memory State

De backend houdt twee objecten bij in het geheugen:

- **devices**  
  `{ [boxId]: { ip, socketId, lastSeen } }`  
  Bevat alle actieve Raspberry Pi's met hun IP, socket-id en laatste heartbeat.

- **commands**  
  `{ [boxId]: { isOn, color, effect, instrument, volume, ... } }`  
  Bevat de laatst ingestelde commandos voor elke box. Deze worden telkens doorgestuurd naar de Pi en frontends bij een update.


## Heartbeat en cleanup

Elke Raspberry Pi stuurt periodiek een `heartbeat` event. De backend bewaart de tijd van de laatste heartbeat per box.  
Komt er langer dan 60 seconden geen heartbeat van een box, dan wordt deze automatisch verwijderd uit de device-lijst en krijgen alle frontends een `device-disconnected` event.

De cleanup gebeurt automatisch elke 30 seconden.

⬅️ [Terug naar overzicht](../README.md#specificaties)