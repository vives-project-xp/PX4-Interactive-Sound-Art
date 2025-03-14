import time, math
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