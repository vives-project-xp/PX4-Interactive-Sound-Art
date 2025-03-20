import time, math , random
from rpi_ws281x import Color

def normalize_hex(hex_color):
    """
    Zorgt ervoor dat de hex kleurstring altijd 6 tekens heeft (zonder de '#' prefix).
    Als de shorthand notatie (3 tekens) wordt gebruikt, wordt deze omgezet naar 6 tekens.
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    if len(hex_color) != 6:
        raise ValueError(f"Ongeldige hex kleur: {hex_color}")
    return hex_color

def effect_chase(strip, leds_to_light, hex_color):
    """
    Chase-effect: Vier opeenvolgende LED's in de ingestelde kleur bewegen door de actieve LEDs.
    Als de actieve zone kleiner is dan 4 LED's, worden er zoveel als mogelijk aangestoken.
    """
    hex_color = normalize_hex(hex_color)
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    chase_speed = 10  # Snelheid van de chase (aantal keer per seconde)
    # Bereken de offset zodat de groep LED's over de actieve zone beweegt
    offset = int(time.time() * chase_speed) % (leds_to_light if leds_to_light > 0 else 1)
    group_size = 4  # Aantal LED's per chase-groep
    
    for i in range(strip.numPixels()):
        if i < leds_to_light and offset <= i < offset + group_size:
            strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2], 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()
    
def effect_fire(strip, leds_to_light):
    """
    Fire-effect: CreÃ«ert een flikkerend vlammen-effect met rood/oranje/gele tinten.
    Dit effect gebruikt geen vaste kleur, maar genereert per LED een random kleur binnen
    een bereik dat bij vuur past.
    """
    import random
    for i in range(strip.numPixels()):
        if i < leds_to_light:
            # Kies een random "vuurkleur" met hoge rood, matige oranje en lage blauw
            green = random.randint(40, 200)
            red = random.randint(200, 255)
            blue = random.randint(0, 50)
            strip.setPixelColor(i, Color(green, red, blue, 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()


def effect_sparkle(strip, leds_to_light, hex_color):
    """
    Sparkle-effect: In de actieve LED-regio knippert een willekeurige subset in de ingestelde kleur.
    Alleen ongeveer 20% van de LEDs krijgt op een gegeven moment de kleur.
    """
    hex_color = normalize_hex(hex_color)
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Zet eerst alle LED's uit
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0, 0))
    # Laat willekeurige LED's oplichten
    for i in range(leds_to_light):
        if random.random() < 0.2:
            strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2], 0))
    strip.show()


def effect_solid(strip, leds_to_light, hex_color):
    hex_color = normalize_hex(hex_color)
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    for i in range(strip.numPixels()):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2], 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def effect_puls(strip, leds_to_light, hex_color):
    import time, math
    period = 2.0  # Puls-periode in seconden
    brightness_factor = 0.35 * (math.sin(2 * math.pi * time.time() / period) + 1) + 0.3
    hex_color = normalize_hex(hex_color)
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    puls_color = tuple(min(255, int(c * brightness_factor)) for c in rgb_color)
    for i in range(strip.numPixels()):
        if i < leds_to_light:
            strip.setPixelColor(i, Color(puls_color[0], puls_color[1], puls_color[2], 0))
        else:
            strip.setPixelColor(i, Color(0, 0, 0, 0))
    strip.show()

def color_wheel(pos):
    from rpi_ws281x import Color
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

def effect_idle(strip):
    """
    Idle-effect: Laat de LEDs één voor één oplichten en weer uitgaan over de volledige LED-strip.
    Dit effect werkt onafhankelijk van de afstand.
    """
    num_leds = strip.numPixels()
    delay = 0.05  # Tijd in seconden tussen elke LED
    
    for i in range(num_leds):
        strip.setPixelColor(i, Color(255, 100, 0, 0))  # Oranje kleur
        strip.show()
        time.sleep(delay)

    for i in range(num_leds):
        strip.setPixelColor(i, Color(0, 0, 0, 0))  # LED uitzetten
        strip.show()
        time.sleep(delay)
