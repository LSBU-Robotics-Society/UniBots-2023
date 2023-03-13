#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <HCSR04.h>

HCSR04 hc(6, new int[3]{ 7, 8, 9 }, 3);  //initialisation class HCSR04 (trig pin , echo pin, number of sensor)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 150   // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 600   // This is the 'maximum' pulse length count (out of 4096)
#define USMIN 600      // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX 2400     // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50  // Analog servos run at ~50 Hz updates

#define motor1Pin1 2
#define motor1Pin2 3
#define motor2Pin1 4
#define motor2Pin2 5

const int PROXIMITYDISTANCE = 10;

String InputDataString;

void servoInit() {
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  delay(10);
}

void setServoAngle(uint8_t n, double angle) {
  double pulselength;
  double pulse;
  pulse = map(angle, 0, 180, USMIN, USMAX);
  pwm.writeMicroseconds(n, pulse);
}

void gateMove(int up) {
  if (up == 1) {
    setServoAngle(0, 0);
    setServoAngle(1, 90);
  } else if (up == 0) {
    setServoAngle(0, 90);
    setServoAngle(1, 0);
  }
}


void motorsInit() {
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin1, OUTPUT);

  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
}

void motorRun(bool motor, bool direction, bool on) {
  if (motor == 0) {
    if (on) {
      if (direction == 0) {
        digitalWrite(motor1Pin1, HIGH);
        digitalWrite(motor1Pin2, LOW);
      } else {
        digitalWrite(motor1Pin1, LOW);
        digitalWrite(motor1Pin2, HIGH);
      }
    } else {
      digitalWrite(motor1Pin1, LOW);
      digitalWrite(motor1Pin2, LOW);
    }
  } else {
    if (on) {
      if (direction == 0) {
        digitalWrite(motor2Pin1, HIGH);
        digitalWrite(motor2Pin2, LOW);
      } else {
        digitalWrite(motor2Pin1, LOW);
        digitalWrite(motor2Pin2, HIGH);
      }
    } else {
      digitalWrite(motor2Pin1, LOW);
      digitalWrite(motor2Pin2, LOW);
    }
  }
}

bool checkCollision(int sensorIndex) {
  if (hc.dist(sensorIndex) < PROXIMITYDISTANCE) {
    //Serial.print(hc.dist(sensorIndex));
    return true;
  } else {
    //Serial.print(hc.dist(sensorIndex));
    return false;
  }
}


String parseString(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}


void checkSerial() {
  if (Serial.available()) {
    InputDataString = Serial.readString();
    DecodeInputString(InputDataString);
  }
}

void DecodeInputString(String InputString) {
  if (InputString.charAt(0) == 'm') {


    int motorCommand = parseString(InputString, ' ', 1).toInt();
    if (motorCommand == 0) { //forward
      motorRun(0, 1, 1);
      motorRun(1, 0, 1);
    } else if (motorCommand == 1) { //backward
      motorRun(0, 0, 1);
      motorRun(1, 1, 1);
    } else if (motorCommand == 2) { //left
      motorRun(0, 1, 1);
      motorRun(1, 1, 1);
    } else if (motorCommand == 3) { //right
      motorRun(0, 0, 1);
      motorRun(1, 0, 1);
    } else if (motorCommand == 4) { //stop
      motorRun(0, 1, 0);
      motorRun(1, 0, 0);
    }

    Serial.print("motor  ");
    Serial.println(motorCommand);
  }

  if (InputString.charAt(0) == 'g') {
    int gateCommand = parseString(InputString, ' ', 1).toInt();
    if (gateCommand ==  1) {
      gateMove(1);
      Serial.print("gate  ");
      Serial.println(gateCommand);
    } else if (gateCommand == 0) {
      gateMove(0);
    }
    Serial.print("gate  ");
    Serial.println(gateCommand);
    
  }

  if (InputString.charAt(0) == 'c') {
    int sensorIndex = parseString(InputString, ' ', 1).toInt();
    bool collision = checkCollision(sensorIndex);
    Serial.println(collision);
  }
}


void setup() {
  Serial.begin(9600);
  motorsInit();
  servoInit();
}

void loop() {
  checkSerial();
}
