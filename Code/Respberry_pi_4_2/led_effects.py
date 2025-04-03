import time, math, random
from rpi_ws281x import Color

def normalize_hex(hex_color):
    """
    Zet een hex kleurstring (bijv. "#F00" of "#FF0000") om in een tuple (r, g, b).
    De shorthand notatie (3 tekens) wordt automatisch uitgebreid naar 6 tekens.
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    if len(hex_color) != 6:
        raise ValueError(f"Ongeldige hex kleur: {hex_color}")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (g, r, b)

def effect_solid(strip, leds_to_light, hex_color):
    rgb_color = normalize_hex(hex_color)
    for i in range(strip.numPixels()):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2], 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def effect_puls(strip, leds_to_light, hex_color):
    period = 2.0  # Puls-periode in seconden
    brightness_factor = 0.35 * (math.sin(2 * math.pi * time.time() / period) + 1) + 0.3
    rgb_color = normalize_hex(hex_color)
    puls_color = (min(255, int(rgb_color[0] * brightness_factor)),
                  min(255, int(rgb_color[1] * brightness_factor)),
                  min(255, int(rgb_color[2] * brightness_factor)))
    for i in range(strip.numPixels()):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(puls_color[0], puls_color[1], puls_color[2], 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def color_wheel(pos):
    # Retourneert een Color gebaseerd op een positie 0-255
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3, 0)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3, 0)

def effect_rainbow(strip, leds_to_light):
    offset = int(time.time() * 50) % 256
    for i in range(leds_to_light):
        pos = ((i * 256 // strip.numPixels()) + offset) & 255
        strip.setPixelColor(i, color_wheel(pos))
    for i in range(leds_to_light, strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def effect_chase(strip, leds_to_light, hex_color):
    rgb_color = normalize_hex(hex_color)
    chase_speed = 10  # Aantal keren per seconde
    offset = int(time.time() * chase_speed) % (leds_to_light if leds_to_light > 0 else 1)
    group_size = 4  # Vier LED's in een groep
    for i in range(strip.numPixels()):
        if i < leds_to_light and offset <= i < offset + group_size:
            strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2], 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def effect_fire(strip, leds_to_light):
    for i in range(strip.numPixels()):
        if i < leds_to_light:
            red = random.randint(200, 255)
            green = random.randint(40, 100)
            blue = random.randint(0, 20)
            strip.setPixelColor(i, Color(green, red, blue, 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def effect_sparkle(strip, leds_to_light, hex_color):
    rgb_color = normalize_hex(hex_color)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0, 0))
    for i in range(leds_to_light):
        if random.random() < 0.2:
            strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2], 0))
    strip.show()

# IdleEffect: Adem/idle effect waarbij alle LED's één voor één opgaan en weer uitgaan.
class IdleEffect:
    def __init__(self, strip, idle_color=(255, 255, 0), delay=0.05):
        """
        IdleEffect bouwt de volledige LED-strip op door alle LED's één voor één aan te zetten 
        en vervolgens weer uit te schakelen. Na een volledige cyclus wordt de idle_color willekeurig vernieuwd.
        
        Parameters:
        - strip: Het LED-strip object.
        - idle_color: Startkleur als tuple (r, g, b).
        - delay: Tijd tussen stappen (in seconden).
        """
        self.strip = strip
        self.idle_color = idle_color
        self.num_leds = strip.numPixels()
        self.state = "build_on"  # "build_on" of "build_off"
        self.current_index = 0
        self.delay = delay
        self.last_update = time.time()

    def update(self):
        """Voert één stap uit van het idle-effect als de ingestelde vertraging is verstreken."""
        now = time.time()
        if now - self.last_update < self.delay:
            return
        self.last_update = now
        if self.state == "build_on":
            # Zet de LED op current_index aan
            self.strip.setPixelColor(self.current_index, Color(self.idle_color[0], self.idle_color[1], self.idle_color[2], 0))
            self.strip.show()
            self.current_index += 1
            if self.current_index >= self.num_leds:
                self.state = "build_off"
                self.current_index = self.num_leds - 1
        elif self.state == "build_off":
            # Zet de LED op current_index uit
            self.strip.setPixelColor(self.current_index, Color(0, 0, 0, 0))
            self.strip.show()
            self.current_index -= 1
            if self.current_index < 0:
                self.state = "build_on"
                self.current_index = 0
                # Vernieuw de idle kleur na een volledige cyclus
                self.idle_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
