# How to add extra light effects?
**Step 1 : make ur effect in the library**

 First u need to know if u need to chose a collor for ur effect , for example in rainbow u don't need to chose a color. Then in the ``led_effects.py`` script u need to add ur   

```
 def UrNewEffect(strip, leds_to_light, hex_color):
```
- leds_to_light = amount of leds that need to be on
- hex_color = the color the user wants in hex (not always needed for effects like rainbow)
- strip = use ``Strip.SetPixelColor(i , Color(0,0,0,0))`` to set colors

**Step 2 : add code to main.py file**