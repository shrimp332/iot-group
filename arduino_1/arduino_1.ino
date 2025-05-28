#include <Wire.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#include <ArduinoJson.h>

Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(2000);


  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 not found at address 0x76");
    delay(1000);
    NVIC_SystemReset(); // ARM reset board
  }
}

void loop() {
  JsonDocument doc;
  doc["temp"] = bmp.readTemperature();
  doc["pressure"] = bmp.readPressure() / 100.0F;
  serializeJson(doc, Serial);
  Serial.println();
  delay(2000);
}
