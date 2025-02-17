#define TRIG_PIN 5  // Trig naar GPIO 5
#define ECHO_PIN 18 // Echo naar GPIO 18 (via spanningsdeler)

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = (duration / 2) / 29.1;; // Omrekenen naar cm

    Serial.print("Afstand: ");
    Serial.print(distance);
    Serial.println(" cm");

    delay(1000);
}
