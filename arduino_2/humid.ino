#include <LiquidCrystal.h>
#include <DHT.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

#define DHTPIN 7
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

String inputMsg = "";
bool msgReceived = false;
String lastWarning = "";

void setup() {
  lcd.begin(16, 2);
  lcd.clear();
  dht.begin();
  Serial.begin(9600);
  inputMsg.reserve(100);
}

void loop() {
  // Handle incoming serial from ThingsBoard
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      msgReceived = true;
      break;
    } else {
      inputMsg += inChar;
    }
  }

  if (msgReceived) {
    if (inputMsg.indexOf("Humidity is too high") != -1) {
      lastWarning = "Humidity is too high";
    } else {
      lastWarning = "";
    }
    inputMsg = "";
    msgReceived = false;
  }

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error");
    delay(2000);
    return;
  }

  lcd.clear();
  if (lastWarning != "") {
    lcd.setCursor(0, 0);
    lcd.print("WARNING:");
    lcd.setCursor(0, 1);
    lcd.print(lastWarning.substring(0, 16));  // truncate if too long
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperature, 1);
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("Hum: ");
    lcd.print(humidity, 1);
    lcd.print("%");
  }

  Serial.print("\"temperature\": ");
  Serial.print(temperature, 2);
  Serial.print(", ");
  Serial.print("\"humidity\": ");
  Serial.println(humidity, 2);
  Serial.println();

  delay(2000);
}
