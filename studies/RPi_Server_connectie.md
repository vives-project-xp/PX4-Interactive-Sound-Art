# **Probleemstelling**
De Soundbox moet verbinding maken met de schoolserver, waarop de website wordt gehost. Dit stelt gebruikers in staat om via hun telefoon lichteffecten en geluiden te kiezen. De uitdaging is om de Raspberry Pi op een betrouwbare manier te laten communiceren met de Express.js backend op de schoolserver.

---

## **Mogelijke verbindingsopties**

### **1️⃣ WiFi (HTTP REST API - Simpel en Betrouwbaar)**
De Raspberry Pi maakt verbinding met het WiFi-netwerk en stuurt HTTP-verzoeken naar de Express.js backend.

**✅ Voordelen:**
- Makkelijk te implementeren met `fetch()` (JavaScript) of `requests` (Python).
- Werkt op elk netwerk zolang de Pi een IP-adres krijgt.
- Schaalbaar: meerdere Soundboxen kunnen via hetzelfde systeem werken.

**❌ Nadelen:**
- Vereist dat de schoolserver het IP van de Pi kan bereiken (mogelijk firewall-configuratie nodig).
- Kleine vertraging bij updates (afhankelijk van polling-frequentie).

### **2️⃣ WebSockets (Realtime, Sneller dan Polling)**
De Raspberry Pi maakt een continue WebSocket-verbinding met de Express.js backend. De server kan direct veranderingen pushen naar de Pi.

**✅ Voordelen:**
- Realtime updates zonder vertraging.
- Efficiënter dan constant HTTP-requests sturen (polling).

**❌ Nadelen:**
- Vereist WebSocket-ondersteuning in Express.js en Python.
- Schoolnetwerk moet WebSockets toestaan.
- Complexer op te zetten dan een REST API.

### **3️⃣ MQTT (Voor Complexe Netwerken, IoT-Stijl)**
De schoolserver draait een MQTT-broker (bijv. Mosquitto) en de Pi luistert naar berichten.

**✅ Voordelen:**
- Betrouwbaar en schaalbaar.
- Makkelijk te integreren in IoT-netwerken.

**❌ Nadelen:**
- Vereist dat er een MQTT-server (broker) draait op de schoolserver.
- Meer configuratie nodig dan REST of WebSockets.