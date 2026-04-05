#include <Servo.h>

Servo myServo;
int pos = 90;

const int step = 1; // Movement increment

void setup() {
  myServo.attach(9);
  myServo.write(pos);
  Serial.begin(9600);
  Serial.println("Servo ready.");
}

void loop() {
  if (Serial.available()) {
    int offset = Serial.parseInt();
    Serial.print("Received: ");
    Serial.println(offset);

    if (offset < -50) {
      pos = constrain(pos + step, 0, 180);
      myServo.write(pos);
    }
    else if (offset > 50) {
      pos = constrain(pos - step, 0, 180);
      myServo.write(pos);
    }
  }
}
