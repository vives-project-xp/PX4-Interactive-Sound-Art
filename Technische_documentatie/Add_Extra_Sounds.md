# How to add extra sounds?
In this part u wil learn how to add extra Sounds to ur Project.

## Add the code in the Pi4
**Step 1 : Put the sound in the right folder**

Start with placing ur folder with the sound in this folder ``home/RPI2/Documents/Sound``. 
![Fysieke_box](./images/Sound_Folder.png)

U will also need **8** different tones of ur sound. And they have to be called ``niveau 1.mp3``, ``niveau 2.mp3``, ``niveau 3.mp3``, .... ,``niveau 8.mp3``.
**Niveau 1 will play with the lowest distance. And niveau 8 with the highest distance.**

![Fysieke_box](./images/New_Sound_Folder.png)

**Step 2 : Add ur sound in the ``sound_player.py``**
```
instruments = {
    "gitaar": load_instrument_sounds("gitaar"),
    "drum": load_instrument_sounds("drum"),
    "bass jumpy": load_instrument_sounds("bass jumpy"),
    "bell": load_instrument_sounds("bell"),
    "synth Sci-Fi": load_instrument_sounds("synth Sci-Fi"),
    "synth sharp": load_instrument_sounds("synth sharp"),
    "bassline": load_instrument_sounds("bassline"),
    "UrNewSound": load_instrument_sounds("UrNewSound")    
}
```
 ### How to change distance settings

 If u want to change the discance at with the sounds play, u can do that in the ``get_level()`` function in the main.py file.
```
def get_level(distance):
    if distance < 10:
        #print(f"Speelt sample niveau 1 af (afstand < 10)")
        return 1
    elif 10 <= distance < 20:
        #print(f"Speelt sample niveau 2 af (afstand 10-20)")
        return 2
    elif 20 <= distance < 30:
        #print(f"Speelt sample niveau 3 af (afstand 20-30)")
        return 3
    elif 30 <= distance < 40:
        #print(f"Speelt sample niveau 4 af (afstand 30-40)")
        return 4
    elif 40 <= distance < 50:
        #print(f"Speelt sample niveau 5 af (afstand 40-50)")
        return 5
    elif 50 <= distance < 60:
        #print(f"Speelt sample niveau 6 af (afstand 50-60)")
        return 6
    elif 60 <= distance < 70:
        #print(f"Speelt sample niveau 7 af (afstand 60-70)")
        return 7
    elif distance >= 70:
        #print(f"Speelt sample niveau 8 af (afstand >= 70)")
        return 8        
```
