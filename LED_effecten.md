## LED - effecten door gebruik van de rpi-ws281x-npm module
 
 # Installeren van de module op de PI
 
 npm install rpi-ws281x-native
 
 # Code voor de LEDs naar een ander kleur te veranderen ( uit te testen )  
 const ws281x = require('rpi-ws281x-native');
 
 const channel = ws281x(100, { stripType: ws281x.stripType.SK6812W });
 
 const colorArray = channel.array;
 
 for (let i = 0; i < channel.count; i++) {
   const red = 0xff;   
   const green = 0xcc; 
   const blue = 0x22; 
   const white = 0x00; 
 
   colorArray[i] = (white << 24) | (red << 16) | (green << 8) | blue;
 }
 
 ws281x.render();
 
 Voor andere kleuren moeten de const red green blue en white aangepast worden
 
 # Rainbow.js gebruiken op de site die Joren in trello heeft gezet
 
 https://www.npmjs.com/package/rpi-ws281x-native?activeTab=code
 
 # iterate.js zorgt voor één LED die beweegt over de LED-strip
 
 Mogelijke aanpassingen:
 
 pixelData[offset] = 0x0000ff;  // Hex code aanpassen naar de kleur die je wilt (in dit geval blauw ipv wit )
 
 pixelData[offset] = 0xff0000;  
 pixelData[(offset + 1) % NUM_LEDS] = 0x00ff00; 
 pixelData[(offset + 2) % NUM_LEDS] = 0x0000ff;   
 --> Meer dan 1 LED gebruiken in verschillende kleuren
 
 Snelheid wijzigen door intervaltijd aan te passen
 
 # brightness.js zorgt voor een verandering in helderheid van LEDs
 
 # Zijn deze .js files te combineren?
 
 # Code voor regenboog effect ( uit te testen ) ( chatGPT )
 
 const ws281x = require('rpi-ws281x-native');
 
 const NUM_LEDS = 60;
 
 const pixelData = new Uint32Array(NUM_LEDS);
 
 ws281x.init(NUM_LEDS, { stripType: ws281x.stripType.SK6812W });
 
 function rainbowEffect() {
     let offset = 0;
 
     setInterval(() => {
         for (let i = 0; i < NUM_LEDS; i++) {
             const red = Math.sin(0.3 * (i + offset)) * 127 + 128;
             const green = Math.sin(0.3 * (i + offset) + 2) * 127 + 128;
             const blue = Math.sin(0.3 * (i + offset) + 4) * 127 + 128;
             const white = Math.sin(0.3 * (i + offset) + 6) * 127 + 128;
 
             pixelData[i] = (white << 24) | (red << 16) | (green << 8) | blue;
         }
 
         ws281x.render(pixelData);
 
         offset++;
     }, 100); 
 }
 
 rainbowEffect();
 
 process.on('SIGINT', () => {
     ws281x.reset();
     process.exit(0);
 });
 
 Const NUM_LEDS aanpassen naar het aantal gebruikte leds  
 
 # Code voor vuurwerk effect ( uit te testen ) ( chatGPT )
 
 const ws281x = require('rpi-ws281x-native');
 
 const NUM_LEDS = 60;
 
 const pixelData = new Uint32Array(NUM_LEDS);
 
 ws281x.init(NUM_LEDS, { stripType: ws281x.stripType.SK6812W });
 
 function random(min, max) {
     return Math.floor(Math.random() * (max - min + 1)) + min;
 }
 
 function getRandomColor() {
     const red = random(100, 255); 
     const green = random(100, 255);
     const blue = random(100, 255);
     const white = random(0, 50);  
     return { red, green, blue, white };
 }
 function fireworkEffect() {
     const interval = setInterval(() => {
         const explosionPos = random(0, NUM_LEDS - 1);
         const explosionColor = getRandomColor();
 
         for (let i = -2; i <= 2; i++) {
             const pos = explosionPos + i;
             if (pos >= 0 && pos < NUM_LEDS) {
                 const color = explosionColor;
                 pixelData[pos] = (color.white << 24) | (color.red << 16) | (color.green << 8) | color.blue;
             }
         }
         ws281x.render(pixelData);
 
         setTimeout(() => {
             for (let i = 0; i < NUM_LEDS; i++) {
                 let color = pixelData[i];
 
                 let red = (color >> 16) & 0xff;
                 let green = (color >> 8) & 0xff;
                 let blue = color & 0xff;
                 let white = (color >> 24) & 0xff;
 
                 red = Math.max(0, red - 15);
                 green = Math.max(0, green - 15);
                 blue = Math.max(0, blue - 15);
                 white = Math.max(0, white - 5);
 
                 pixelData[i] = (white << 24) | (red << 16) | (green << 8) | blue;
             }ws281x.render(pixelData);
         }, 100);
     }, 500);
     
     process.on('SIGINT', () => {
         clearInterval(interval);
         ws281x.reset();
         process.exit(0);
     });
 }
 
 fireworkEffect();
 