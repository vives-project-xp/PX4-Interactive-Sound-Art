# Uploading and Using MP3 Files in the Interactive Sound Art Interface

## Introduction
This document outlines the steps required to enable MP3 file uploads via the frontend interface and use them for playback on the Raspberry Pi (RPi) sound box. The implementation involves changes to both the frontend and backend components of the project, with WebSocket integration for real-time communication.

---

## Frontend Implementation

### 1. Add an MP3 Upload Component
Create a new Vue component for uploading MP3 files. This component will allow users to select and upload MP3 files.

```vue
<template>
  <div class="upload-container">
    <h2>Upload MP3 File</h2>
    <input type="file" accept="audio/mp3" @change="handleFileUpload" />
    <button @click="uploadFile">Upload</button>
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
          alert("File uploaded successfully!");
          // Notify backend via WebSocket
          socket.emit("mp3Uploaded", { fileName: this.selectedFile.name });
        } catch (error) {
          console.error("Error uploading file:", error);
          alert("Failed to upload file.");
        }
      } else {
        alert("Please select a file first.");
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
Add a new method to handle MP3 file uploads.

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
    console.warn("Failed to upload MP3 file:", error.message);
    throw error;
  }
}
```

### 3. Integrate the Upload Component
Include the new upload component in the main application.

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

## Backend Implementation

### 1. Add an MP3 Upload Endpoint
Update the backend to handle MP3 file uploads. Use the `express-fileupload` middleware for handling file uploads.
## Manipulate the mp3 for different pitches

````python
from pydub import AudioSegment
from pydub.playback import play
import os

def change_pitch(sound, semitones):
    """
    Change the pitch of an audio file by a given number of semitones.
    Positive semitones increase pitch, negative decrease pitch.
    """
    new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
    return sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate}).set_frame_rate(sound.frame_rate)

def create_pitched_versions(input_file, output_folder):
    """
    Create 8 different pitch versions of the input MP3 file.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the MP3 file
    sound = AudioSegment.from_file(input_file)

    # Generate 8 pitch variations
    for i, semitones in enumerate(range(-4, 4), start=1):  # -4 to +3 semitones
        pitched_sound = change_pitch(sound, semitones)
        output_file = os.path.join(output_folder, f"niveau {i}.mp3")
        pitched_sound.export(output_file, format="mp3")
        print(f"Saved: {output_file}")

# Example usage
input_mp3 = "path/to/your/input.mp3"  # Replace with your MP3 file path
output_dir = "path/to/output/folder"  # Replace with your desired output folder
create_pitched_versions(input_mp3, output_dir)
````

#### Install Dependencies
```bash
npm install express-fileupload
```

#### Update `index.js`
Add the following code to handle MP3 uploads and notify clients via WebSocket:

```js
import fileUpload from "express-fileupload";
import { Server } from "socket.io";

app.use(fileUpload());
const io = new Server(server);

app.post("/upload-mp3", (req, res) => {
  if (!req.files || !req.files.file) {
    return res.status(400).send("No file uploaded.");
  }

  const mp3File = req.files.file;
  const uploadPath = `/home/RPI2/Documents/Sounds/${mp3File.name}`;

  mp3File.mv(uploadPath, (err) => {
    if (err) {
      console.error("Error saving file:", err);
      return res.status(500).send("Failed to upload file.");
    }
    res.send("File uploaded successfully.");
    // Notify all connected clients
    io.emit("mp3Uploaded", { fileName: mp3File.name });
  });
});
```

---

## Raspberry Pi Integration

### 1. Update `sound_player.py`
Modify the `sound_player.py` script to dynamically load and play uploaded MP3 files upon receiving WebSocket events.

```python
import os
import pygame
import socketio

# Initialize pygame mixer
pygame.mixer.init()

SOUNDS_BASE_PATH = "/home/RPI2/Documents/Sounds"
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to backend via WebSocket")

@sio.event
def mp3Uploaded(data):
    file_name = data.get("fileName")
    if file_name:
        play_uploaded_sound(file_name)

@sio.event
def disconnect():
    print("Disconnected from backend")

def play_uploaded_sound(file_name):
    file_path = os.path.join(SOUNDS_BASE_PATH, file_name)
    if os.path.exists(file_path):
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        print(f"Playing {file_name}")
    else:
        print(f"File {file_name} not found.")

# Connect to the WebSocket server
sio.connect("http://localhost:4000")
```

---

## Conclusion
By following the steps outlined above, you can enable MP3 file uploads via the frontend interface and use them for playback on the Raspberry Pi sound box. The integration of WebSockets ensures real-time communication between the frontend, backend, and Raspberry Pi.