# MP3 Bestanden Uploaden en Gebruiken in de Interactieve Geluidskunst Interface

# Moeilijkheden 
- 1) Er zal real time audio manipulatie moeten gebeuren, wat een hoop andere complexiteiten met zich meebrengt (geluid moet goed zijn, zal het niet slecht klinken, zal er geen delay daardoor komen etc...)
- 2) Een inlogsysteem moet worden geïmplementeerd om te beheren wie toegang heeft tot de "upload" functie.
    Dit brengt wel extra complexiteit met zich mee.

---

## Frontend Implementatie

### 1. Een MP3 Upload Component Toevoegen
Creëer een nieuw Vue-component voor het uploaden van MP3-bestanden. Dit component zal gebruikers in staat stellen om MP3-bestanden te selecteren en te uploaden.

```vue
<template>
  <div class="upload-container">
    <h2>Upload MP3 Bestand</h2>
    <input type="file" accept="audio/mp3" @change="handleFileUpload" />
    <button @click="uploadFile">Uploaden</button>
  </div>
</template>

<script>
import apiService from "../services/apiService";
import socket from "../socket";

export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (this.selectedFile) {
        const formData = new FormData();
        formData.append("file", this.selectedFile);
        try {
          await apiService.uploadMP3(formData);
          alert("Bestand succesvol geüpload!");
          // Backend informeren via WebSocket
          socket.emit("mp3Uploaded", { fileName: this.selectedFile.name });
        } catch (error) {
          console.error("Fout bij uploaden bestand:", error);
          alert("Uploaden van bestand mislukt.");
        }
      } else {
        alert("Selecteer eerst een bestand.");
      }
    },
  },
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style>
```

### 2. Update `apiService.js`
Voeg een nieuwe methode toe om MP3-bestandsuploads te verwerken.

```js
async uploadMP3(fileData) {
  try {
    const response = await axios.post(`${API_URL}/upload-mp3`, fileData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.warn("MP3 bestand uploaden mislukt:", error.message);
    throw error;
  }
}
```

### 3. Integreer het Upload Component
Neem het nieuwe uploadcomponent op in de hoofdapplicatie.

```vue
<template>
  <div id="app">
    <MusicBoxSelector />
    <MP3Upload />
  </div>
</template>

<script>
import MusicBoxSelector from "./components/MusicBoxSelector.vue";
import MP3Upload from "./components/MP3Upload.vue";

export default {
  components: {
    MusicBoxSelector,
    MP3Upload,
  },
};
</script>
```

---

## Backend Implementatie

### 1. Een MP3 Upload Eindpunt Toevoegen
Werk de backend bij om MP3-bestandsuploads te verwerken. Gebruik de `express-fileupload` middleware voor het verwerken van bestandsuploads.
## MP3 manipuleren voor verschillende toonhoogtes

````python
from pydub import AudioSegment
from pydub.playback import play
import os

def change_pitch(sound, semitones):
    """
    Verander de toonhoogte van een audiobestand met een bepaald aantal halve tonen.
    Positieve waardes verhogen de toonhoogte, negatieve verlagen deze.
    """
    new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
    return sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate}).set_frame_rate(sound.frame_rate)

def create_pitched_versions(input_file, output_folder):
    """
    Maak 8 verschillende toonhoogte-versies van het input MP3-bestand.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Laad het MP3-bestand
    sound = AudioSegment.from_file(input_file)

    # Genereer 8 toonhoogte-variaties
    for i, semitones in enumerate(range(-4, 4), start=1):  # -4 tot +3 halve tonen
        pitched_sound = change_pitch(sound, semitones)
        output_file = os.path.join(output_folder, f"niveau {i}.mp3")
        pitched_sound.export(output_file, format="mp3")
        print(f"Opgeslagen: {output_file}")

# Voorbeeld gebruik
input_mp3 = "pad/naar/jouw/input.mp3"  # Vervang met het pad naar jouw MP3-bestand
output_dir = "pad/naar/output/map"  # Vervang met je gewenste output map
create_pitched_versions(input_mp3, output_dir)
````

#### Installeer Afhankelijkheden
```bash
npm install express-fileupload
```

#### Update `index.js`
Voeg de volgende code toe om MP3-uploads te verwerken en clients te informeren via WebSocket:

```js
import fileUpload from "express-fileupload";
import { Server } from "socket.io";

app.use(fileUpload());
const io = new Server(server);

app.post("/upload-mp3", (req, res) => {
  if (!req.files || !req.files.file) {
    return res.status(400).send("Geen bestand geüpload.");
  }

  const mp3File = req.files.file;
  const uploadPath = `/home/RPI2/Documents/Sounds/${mp3File.name}`;

  mp3File.mv(uploadPath, (err) => {
    if (err) {
      console.error("Fout bij opslaan bestand:", err);
      return res.status(500).send("Uploaden van bestand mislukt.");
    }
    res.send("Bestand succesvol geüpload.");
    // Informeer alle verbonden clients
    io.emit("mp3Uploaded", { fileName: mp3File.name });
  });
});
```

---

## Raspberry Pi Integratie

### 1. Update `sound_player.py`
Wijzig het `sound_player.py` script om dynamisch geüploade MP3-bestanden te laden en af te spelen bij het ontvangen van WebSocket-events.

```python
import os
import pygame
import socketio

# Initialiseer pygame mixer
pygame.mixer.init()

SOUNDS_BASE_PATH = "/home/RPI2/Documents/Sounds"
sio = socketio.Client()

@sio.event
def connect():
    print("Verbonden met backend via WebSocket")

@sio.event
def mp3Uploaded(data):
    file_name = data.get("fileName")
    if file_name:
        play_uploaded_sound(file_name)

@sio.event
def disconnect():
    print("Verbinding met backend verbroken")

def play_uploaded_sound(file_name):
    file_path = os.path.join(SOUNDS_BASE_PATH, file_name)
    if os.path.exists(file_path):
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        print(f"Speelt {file_name} af")
    else:
        print(f"Bestand {file_name} niet gevonden.")

# Verbind met de WebSocket server
sio.connect("http://localhost:4000")
```

---

## Conclusie
Door de hierboven beschreven stappen te volgen, kun je MP3-bestandsuploads via de frontend-interface mogelijk maken en ze afspelen op de Raspberry Pi geluidsbox. De integratie van WebSockets zorgt voor realtime communicatie tussen de frontend, backend en Raspberry Pi.