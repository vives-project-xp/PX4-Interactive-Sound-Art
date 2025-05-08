# PX4-Interactive-Sound-Art

PX4-Interactive-Sound-Art is een interactief kunstproject dat beweging, geluid en visuele feedback combineert. Door handbewegingen boven een sensor worden geluiden afgespeeld en lichtpatronen geactiveerd.

## Team

- Maxime Coen
- Michiel Geeraert
- William Rogov
- Sam De Wispeleare
- Thorben Andries
- Timo Plets
- Ward Dereeper
- Joren Vandewalle

## Doel

Het doel van dit project is om een interactieve sound-art installatie te creëren waarin gebruikers door handbewegingen muziek en licht kunnen beïnvloeden.

## Hoe werkt het?

- Een sensor detecteert handbewegingen boven het apparaat.

- De afstand van de hand bepaalt de toonhoogte of het type geluid.

- Tegelijkertijd reageert een LED-strip met kleur en lichtpatronen.


## Materialen lijst

Dit is voor 1 unit.

- Raspberry Pi 4
- 5V Ledstrip (individually addressable)
- MDF platen
- Licht verspreidende buis (acryl)
- Speaker
- Digitale versterker voor speaker
- 3.3V -> 5.0V switch
- Verdeelstekker (4 slots per unit)
- Schroeven

Extra info vindt je [hier](./documentatie/Materialen_info.md).

## Fysieke behuizing

Een volledige unit bestaat uit een houten box (MDF) met daarop een acrylen buis. Aan de voorkant van de box zit een speaker, op de bovenkant heb je het gat voor de sensor en achteraan heb je een gat voor de stroomvoorziening.
Voor meerdere unit's te gebruiken kan dit voor stroomvoorziening in elkaar gechained worden.

![Fysieke_box](./studies/fotos/PX4%20ProtoType%20Assembly.png)

### Afmetingen

- Houten doos: 40x40
- Buis lengte: 1m
- Diameter buis: 10 cm
- Diameter speaker gat: 20,5 cm
- Sensor gat: 4,5x4,5 cm

## Software

We gebruiken per unit een Raspberry Pi 4. Dit zal er voor zorgen dat we den waarde van de sensor (afstand hand) kunnen omrekenen naar een geluid en signaal voor de leds. Er worden mp3 bestanden gebruikt met tonen voor het geluid te spelen.

## Architectuur: Frontend & Backend

Het project bestaat uit twee belangrijke onderdelen die met elkaar communiceren:

### Frontend

De frontend is gebouwd met Vue.js en biedt een gebruiksvriendelijke interface waarmee:

- Gebruikers verschillende muziekboxen kunnen selecteren en beheren
- De kleur van de LED-verlichting kan worden aangepast
- Het volume kan worden geregeld
- Verschillende geluidseffecten kunnen worden geselecteerd

De interface heeft een modern, donker thema met kleurrijke accenten die passen bij het kunstzinnige karakter van het project.

### Backend

De backend is ontwikkeld met Node.js en Express en fungeert als centraal communicatiepunt tussen de frontend en de Raspberry Pi units:

- Gebruikt WebSockets voor real-time communicatie
- Houdt verbinding met alle aangesloten muziekboxen (Raspberry Pi's)
- Stuurt opdrachten door van de interface naar de juiste unit
- Zorgt voor synchronisatie tussen alle onderdelen

### Communicatie

De communicatie tussen de onderdelen verloopt als volgt:

1. De gebruiker maakt wijzigingen in de web-interface
2. De frontend stuurt deze wijzigingen naar de backend server
3. De backend stuurt de instructies door naar de juiste Raspberry Pi unit
4. De Raspberry Pi past de lichteffecten en het geluid aan

Dit systeem maakt het mogelijk om meerdere muziekboxen vanaf één interface te besturen, wat interactieve installaties met meerdere units mogelijk maakt.

### Server Omgeving

Het volledige systeem draait op een centrale server die toegankelijk is via het netwerk:

- De backend-server zorgt voor de centralisatie van alle data en communicatie
- Docker-containers worden gebruikt voor eenvoudige deployment en schaalbaarheid
- De server-omgeving kan worden opgestart met Docker Compose via het configuratiebestand in de `interface` map
- WebSocket-verbindingen zorgen voor real-time communicatie tussen alle componenten

De server is bereikbaar voor alle gebruikers binnen hetzelfde netwerk, wat verschillende bedieningen mogelijk maakt:
- Via een webbrowser op een laptop of desktop computer
- Met een tablet als controle-interface
- Mogelijkheid tot beheer op afstand voor administrators

Voor details over de server-setup en configuratie, zie [Backend.md](./documentatie/Backend.md).

## Geluidsbibliotheek & Samples

Het project maakt gebruik van een uitgebreide verzameling geluidssamples die georganiseerd zijn in verschillende instrumentcategorieën:

### Sample Structuur

- Elke instrumentcategorie (zoals bass, gitaar, synth, etc.) bevat 8 verschillende samples
- Deze samples zijn genummerd van niveau 1 t/m niveau 8, wat correspondeert met verschillende afstanden van de hand tot de sensor
- Wanneer een gebruiker zijn hand op een bepaalde hoogte houdt, wordt het corresponderende geluidsniveau afgespeeld

### Beschikbare Instrumenten

Het systeem bevat momenteel de volgende instrumentcategorieën:
- Bass (meerdere varianten)
- Bassline
- Bell
- Drum
- Gitaar
- Synth (meerdere varianten)

### Geluid Afspelen

Het geluidssysteem werkt als volgt:
- De afstandssensor bepaalt de hoogte van de hand boven het apparaat
- Deze afstand wordt omgezet naar een van de 8 niveaus
- De bijhorende MP3-sample wordt afgespeeld via de ingebouwde speaker
- Tegelijkertijd worden de LED-effecten gesynchroniseerd met het geluid

Voor het toevoegen van nieuwe geluiden, zie de handleiding in [MP3_Upload_Guide.md](./geluid_uploaden/MP3_Upload_Guide.md).

## Uitbreidingsmogelijkheden

Het PX4-Interactive-Sound-Art project is ontworpen om flexibel te zijn en biedt verschillende mogelijkheden voor uitbreiding:

### Extra Effecten

Het huidige systeem kan worden uitgebreid met meer LED-effecten. Voor ontwikkelaars is er een handleiding beschikbaar onder [Add_Extra_Effects.md](./documentatie/Add_Extra_Effects.md) die uitlegt hoe nieuwe lichtpatronen kunnen worden toegevoegd.

### Nieuwe Geluiden

De geluidsbibliotheek kan worden uitgebreid met:
- Nieuwe instrumenten of geluidscategorieën
- Alternatieve toonladders of modulaties
- Aangepaste geluidseffecten

Volg de [Add_Extra_Sounds.md](./documentatie/Add_Extra_Sounds.md) handleiding voor het toevoegen van nieuwe geluiden aan het systeem.

### Meerdere Units

Het project is ontworpen om te werken met meerdere units die samen een grotere installatie vormen:
- Units kunnen in keten worden geschakeld voor stroomvoorziening
- Via de centrale interface kunnen alle units individueel worden aangestuurd
- Dit maakt creatieve opstellingen mogelijk waarbij verschillende units samen een harmonie creëren

### Toekomstige Ontwikkelingen

Mogelijke richtingen voor verdere ontwikkeling:
- Integratie met MIDI-apparaten voor live performance
- Machine learning voor adaptieve geluidseffecten gebaseerd op gebruikersgedrag
- Mobiele app voor bediening op afstand
- Geavanceerde visualisaties die reageren op de geluiden

## Installatie en Opstarten

Voor instructies over het instellen van de Raspberry Pi, zie [Raspberry_Pi_4_Instellen.md](./Raspberry_Pi_4_Instellen.md).

Voor meer informatie over het uploaden van nieuwe geluiden, zie [MP3_Upload_Guide.md](./geluid_uploaden/MP3_Upload_Guide.md).