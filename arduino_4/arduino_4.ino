const int LDR_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(LDR_PIN);
  Serial.print("LDR Value: ");
  Serial.println(sensorValue);
  delay(500);
} 