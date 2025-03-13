# PX4-Interactive-Sound-Art

PX4-Interactive-Sound-Art is een interactief kunstproject dat beweging, geluid en visuele feedback combineert. Door handbewegingen boven een sensor worden geluiden afgespeeld en lichtpatronen geactiveerd.

## Team

-Maxime Coen
-Michiel Geeraert
-William Rogov
-Sam De Wispeleare
-Thorben Andries
-Timo Plets
-Ward Dereeper
-Joren Vandewalle

## Doel

Het doel van dit project is om een interactieve sound-art installatie te creëren waarin gebruikers door handbewegingen muziek en licht kunnen beïnvloeden.

## Hoe werkt het?

-Een sensor detecteert handbewegingen boven het apparaat.

-De afstand van de hand bepaalt de toonhoogte of het type geluid.

-Tegelijkertijd reageert een LED-strip met kleur en lichtpatronen.


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