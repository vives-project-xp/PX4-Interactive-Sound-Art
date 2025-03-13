const express = require('express');
const bodyParser = require('body-parser');
const ws281x = require('rpi-ws281x-native');

const NUM_LEDS = 60; // Pas aan naar je setup
const pixelData = new Uint32Array(NUM_LEDS);
ws281x.init(NUM_LEDS);

const app = express();
app.use(bodyParser.json());
app.use(require('cors')()); // Voorkom CORS-problemen

// Functie om kleur te zetten
function setColor(hexColor) {
    let color = parseInt(hexColor.replace("#", ""), 16);
    for (let i = 0; i < NUM_LEDS; i++) {
        pixelData[i] = color;
    }
    ws281x.render(pixelData);
}

// API-endpoint voor kleurverandering
app.post('/setColor', (req, res) => {
    const { color } = req.body;
    if (!color) return res.status(400).json({ error: "Geen kleur ontvangen" });

    setColor(color);
    console.log(`LED Kleur gewijzigd naar: ${color}`);
    res.json({ message: `Kleur ingesteld op ${color}` });
});

// Server starten
app.listen(4000, () => console.log("LED server draait op poort 4000"));
