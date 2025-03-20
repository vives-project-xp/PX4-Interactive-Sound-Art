# How to add extra light effects?
In this part u wil learn how to add light effects to ur project.

## Add the code in the Pi4
**Step 1 : make ur effect in the library**

First, determine whether your effect needs a color. For example, in the rainbow effect you don't need to choose a color. Then, in the ``led_effects.py`` script, add your code. For example, you can start with:

```
 def UrNewEffect(strip, leds_to_light, hex_color):
    # Your custom code here.
    # - leds_to_light: the number of LEDs that need to be on.
    # - hex_color: the color in hexadecimal (not needed for effects like rainbow).
    # - strip: use strip.setPixelColor(i, Color(0, 0, 0, 0)) to set colors.

```

From here, you can implement your own effect.

**Step 2 : add code to main.py file**

In your main.py script, import your new effect along with the existing ones:
```
from led_effects import effect_solid, effect_puls, effect_rainbow, effect_chase, effect_fire, effect_sparkle , UrNewEffect
```
Then, update your ``update_leds()`` function to include your effect:

```
def update_leds(distance):
    leds_to_light = int(distance / 1.5)
    
    if current_effect == "solid":
        effect_solid(strip, leds_to_light, current_color)
    elif current_effect == "puls":
        effect_puls(strip, leds_to_light, current_color)
    elif current_effect == "rainbow":
        effect_rainbow(strip, leds_to_light)
    elif current_effect == "chase":
        effect_chase(strip, leds_to_light, current_color)
    elif current_effect == "fire":
        effect_fire(strip, leds_to_light)
    elif current_effect == "sparkle":
        effect_sparkle(strip, leds_to_light, current_color)
    elif current_effect == "UrNewEffect":
        effect_UrNewEffect(strip , leds_to_light,current_color)
    else:
        effect_solid(strip, leds_to_light, current_color)
```
