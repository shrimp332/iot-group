#include <Servo.h>

Servo lidServo;

const int rainSensorPin = 2;    // Digital pin connected to rain sensor DO
const int servoPin = 9;         // PWM pin connected to servo signal


void setup() {
  Serial.begin(9600);
  pinMode(rainSensorPin, INPUT);
  lidServo.attach(servoPin);
  lidServo.write(0); 
}

void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command.startsWith("ANGLE:")) {
      int angle = command.substring(6).toInt();
      angle = constrain(angle, 0, 180); // safety check
      Serial.print("Setting servo angle to: ");
      Serial.println(angle);
      lidServo.write(angle);
    }
  }
  int rainState = digitalRead(rainSensorPin);

  if (rainState == HIGH) {  // Assuming HIGH means rain detected (check your sensor)
    Serial.println("RAIN");
  } else {
    Serial.println("NO_RAIN");
  }

  delay(1000);  // Check every second
}
