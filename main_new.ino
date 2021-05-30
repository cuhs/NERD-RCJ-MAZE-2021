#include "global_vars.h"

void setup() {
  delay(1);
  Serial.begin(9600);
  Serial2.begin(9600);
  Wire.begin();
  Serial2.write('a');
  pinMode(A9, OUTPUT);
  INIT_INTERRUPT(LEFT);
  INIT_INTERRUPT(RIGHT);
  ports[RIGHT].backwards = true;
  Serial.println("--------------------STARTING NOW--------------------");
  setupSensors();
  myservo.attach(A8, 490, 2400); // attaches the servo on pin A8 to the servo object
  midPos();

}



void loop() {

  // (possibly) WORKING CODE VVVVVVVVVVVVVVVVVV


  if (Serial2.available()) {
    delay(1);
    char incoming_byte = Serial2.read();
    delay(1);
    Serial.println("Message detected.");
    if (incoming_byte == 'g') {
      Serial.println("'g' received. Sending wall values.");
      sendWallValues((getSensorReadings(3) + getSensorReadings(1)) / 2, (getSensorReadings(0) + getSensorReadings(4)) / 2, getSensorReadings(2));
    }
    if (incoming_byte == 'm') {
      motorControl();
      Serial2.write('d');
    }
    if (incoming_byte == 'v') {
      digitalWrite(A9, HIGH);
      delay(5000);
      digitalWrite(A15, LOW);
      delay(1);
      char dir = Serial2.read();
      delay(1);
      int packs = Serial2.read() - '0';
      Serial.println("'v' received. Printing victim values.");
      Serial.print("Direction: ");
      Serial.print(dir);
      Serial.print("\tPackages: ");
      Serial.println(packs);
      if (dir == 'R') {
        for (int i = 0; i < packs; i++) {
          turnRight();
          midPos();
        }
      }
      if (dir == 'L') {
        for (int i = 0; i < packs; i++) {
          turnLeft();
          midPos();
        }
      }
    }
  }

}
