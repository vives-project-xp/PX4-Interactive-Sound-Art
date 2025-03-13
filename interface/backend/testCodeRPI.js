from flask import Flask, request, jsonify
import board
import neopixel

app = Flask(__name__)

# Set up LED strip (Change this based on your setup)
LED_PIN = board.D18
NUM_LEDS = 30  # Change based on number of LEDs
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, auto_write=False)

# Function to update LEDs
def update_leds(color, effect):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    
    if effect == "solid":
        pixels.fill((r, g, b))
    elif effect == "strobe":
        for _ in range(10):
            pixels.fill((r, g, b))
            pixels.show()
            time.sleep(0.1)
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.1)
    elif effect == "fire":
        for i in range(NUM_LEDS):
            pixels[i] = (r, g, b) if i % 2 == 0 else (r//2, g//2, b//2)
    pixels.show()

# Route to update LED and sound settings
@app.route("/update", methods=["POST"])
def update():
    data = request.json
    color = data.get("color", "#FFFFFF")
    effect = data.get("effect", "solid")
    
    print(f"🎵 Instrument: {data.get('instrument')} | 🎨 Color: {color} | 💡 Effect: {effect}")
    
    update_leds(color, effect)
    return jsonify({"message": "LEDs updated!"})

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
