const int LDR_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
	int ldrValue = analogRead(LDR_PIN);
	
	// Printing in a JSON format like {"ldr": value}
	Serial.print("{\"ldr\":");
	Serial.print(ldrValue);
	Serial.println("}");
	
	delay(1000);
}