# ✅ Stappenplan: Lokale WebSocket-setup op de Raspberry Pi

Omdat de backend nog niet werkt, kunnen we **lokaal testen en voorbereiden**. Dit bespaart tijd en zorgt ervoor dat we direct kunnen koppelen zodra de backend beschikbaar is.

---

## 🔹 Stap 1: Lokale WebSocket-server opzetten
Om te testen hoe de Raspberry Pi straks met de backend gaat communiceren, bouwen we een **lokale WebSocket-server**. Dit simuleert de echte backend.

### 1️ Maak een nieuw Python-script aan op de Raspberry Pi  
```bash
nano local_websocket_server.py
```

### 2️ Voeg de volgende code toe en sla op (`CTRL + X`, `Y`, `ENTER`)  
```python
import asyncio
import websockets
import json

async def handle_client(websocket, path):
    print("Client verbonden!")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Ontvangen van client: {data}")

            # Simuleer een antwoord zoals de echte backend zou doen
            if data.get("action") == "play_sound":
                response = {"status": "ok", "message": "Geluid wordt afgespeeld"}
            elif data.get("action") == "led_on":
                response = {"status": "ok", "message": "LED is aangezet"}
            else:
                response = {"status": "error", "message": "Onbekend commando"}

            await websocket.send(json.dumps(response))
    
    except websockets.exceptions.ConnectionClosed:
        print("Client heeft de verbinding verbroken.")

start_server = websockets.serve(handle_client, "0.0.0.0", 4000)

print("Lokale WebSocket-server gestart op poort 4000...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

### 3️ Start de WebSocket-server:  
```bash
python3 local_websocket_server.py
```
 **Deze server luistert nu op poort 4000 en simuleert backend-antwoorden!**

---

## 🔹 Stap 2: Raspberry Pi WebSocket-client bouwen
Nu maken we een **client** die berichten naar de testserver stuurt, zoals de echte Raspberry Pi straks met de backend zal doen.

### 1️ Maak een nieuw bestand aan:  
```bash
nano local_websocket_client.py
```

### 2️ Voeg de volgende code toe:  
```python
import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://localhost:4000"

    async with websockets.connect(uri) as websocket:
        # Stuur een testbericht om geluid af te spelen
        message = json.dumps({"action": "play_sound"})
        await websocket.send(message)
        print(f"> Verzonden: {message}")

        # Ontvang en toon het antwoord
        response = await websocket.recv()
        print(f"< Ontvangen: {response}")

asyncio.run(websocket_client())
```

### 3️ Voer de client uit in een tweede terminal:  
```bash
python3 local_websocket_client.py
```
 **De client stuurt nu een bericht naar de lokale server en ontvangt een reactie.**

---

## 🔹 Stap 3: Testen en verbeteren
- Probeer verschillende berichten, zoals:
  ```python
  message = json.dumps({"action": "led_on"})
  ```
- Voeg logging toe om beter te zien wat er gebeurt.
- Test met meerdere clients tegelijk.

---

## 🔹 Stap 4: Voorbereiding op de echte backend
1. Zorg ervoor dat de **Pi verbinding kan maken met het internet** en de schoolserver (`ping 10.10.2.49`).
2. Vraag de backend-ontwikkelaar **welke JSON-structuur** ze gebruiken.
3. Zodra de backend draait, vervang `"ws://localhost:4000"` door `"ws://10.10.2.49:4000"` en test opnieuw.

---

##  Conclusie
 We hebben een **lokale testomgeving opgezet**.  
 Zodra de backend werkt, kunnen we **direct overschakelen** naar de echte verbinding.  
Wil je dat ik help met extra functionaliteiten, zoals logs opslaan of sensoren koppelen? 🚀
