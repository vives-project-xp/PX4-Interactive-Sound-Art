#include <FastLED.h>

// Number of LEDs in your strip
#define NUM_LEDS 100

// Pin for controlling the LEDs
#define DATA_PIN 2

// Define the array of LEDs
CRGB leds[NUM_LEDS];

// Time scaling factors for each component (optional, can be removed if not used)
#define TIME_FACTOR_HUE 60
#define TIME_FACTOR_SAT 100
#define TIME_FACTOR_VAL 100



#define TRIG_PIN 5  // Trig naar GPIO 5
#define ECHO_PIN 18 // Echo naar GPIO 18 (via spanningsdeler)


#define CM_LIGHT 1.5


int TimeOuteCounter = 0;

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);


    // Initialize LEDs with RGBW configuration
    FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS).setRgbw(RgbwDefault());
    FastLED.setBrightness(50);  // Set global brightness to 50%

    // Set all LEDs to purple (mix of red and blue)
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CRGB(0, 0, 0); // Rood , Blauw , Groen
    }
    FastLED.show();  // Update the LEDs
}

void loop() {
    

  
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = (duration / 2) / 29.1;; // Omrekenen naar cm

    

    if(distance > 177){
      TimeOuteCounter++;
    } else{
      TimeOuteCounter=0;
    }


    Serial.print("Afstand: ");
    Serial.print(distance);
    Serial.println(" cm");


    int ledsToLight = distance/ CM_LIGHT;

    Serial.print("Aantal LedsBrandend: ");
    Serial.println(ledsToLight);

    if(TimeOuteCounter < 20 ) {
      for (int i = 0; i < ledsToLight; i++) {
          if (i < NUM_LEDS) {  
              leds[i] = CRGB(255, 255, 0); 
          }
      }

      for (int i = ledsToLight; i < NUM_LEDS; i++) {
          if (i < NUM_LEDS) { 
              leds[i] = CRGB(0, 0, 0); 
          }
      } 
    } else{
        for (int i = 0; i < NUM_LEDS; i++) {
          leds[i] = CRGB(0, 0, 0); // Rood , Blauw , Groen
        }
     }


    FastLED.show();
    delay(250);
}
