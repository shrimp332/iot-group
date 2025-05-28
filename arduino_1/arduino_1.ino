#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 not found at address 0x76");
    while (1);
  }
  Serial.println("BMP280 found!");
}

void loop() {
  Serial.print("Temp: ");
  Serial.print(bmp.readTemperature());
  Serial.print(" °C, Pressure: ");
  Serial.print(bmp.readPressure() / 100.0F);
  Serial.println(" hPa");
  delay(2000);
}
