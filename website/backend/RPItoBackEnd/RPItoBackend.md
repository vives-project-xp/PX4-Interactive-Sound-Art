# Project Status: Raspberry Pi ↔ Backend WebSockets

## Wat hebben we al gedaan?

### **1. Raspberry Pi setup & voorbereiding**
- **WiFi-configuratie:** 
- **Systeemupdates uitgevoerd:**
  ```
  sudo apt update && sudo apt upgrade -y
  ```
- **Benodigde software geïnstalleerd:**
  - Python WebSockets library:
    ```
    sudo apt install python3-websockets
    ```

  - Node.js & npm:
    ```
    sudo apt install nodejs npm -y
    ```

  - WebSocket testtool `wscat` (geïnstalleerd met sudo vanwege rechtenprobleem):
    ```
    sudo npm install -g wscat
    ```


### **2. Eerste connectietests met de backend**
- **Gegevens ontvangen van de backend-ontwikkelaar:**
  - Backend wordt gebouwd met **Express.js**.
  - WebSockets worden gebruikt voor communicatie.
  - **Server draait nog niet**, maar zal later beschikbaar zijn.
  - IP van de Raspberry Pi: `10.10.2.49`
  - WebSocket-poort: `4000`
  
- **Test uitgevoerd met `wscat` om verbinding te maken:**
  ```bash
  wscat -c ws://10.10.2.49:4000
  ```
  **Resultaat:** Kan geen verbinding maken, omdat de backend nog niet draait.