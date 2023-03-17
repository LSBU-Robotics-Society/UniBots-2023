#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <HCSR04.h>
#include "cmd_list.h"

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

#define LED_BLINK_COUNT 200
int LEDcount = LED_BLINK_COUNT;

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

void LEDinit(){
  pinMode(LED_BUILTIN, OUTPUT);
  LEDcount = 0; //Off
}

void LEDupdate(){
  if(LEDcount > 0)
  {
    digitalWrite(LED_BUILTIN, HIGH);
    --LEDcount;
  }
  else
    digitalWrite(LED_BUILTIN, LOW);
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
  while (Serial.available()) {
    InputDataString = Serial.readStringUntil('\n');
    DecodeInputString(InputDataString);
  }
}

void DecodeInputString(String InputString) {

  char Command = InputString.charAt(0);
  
  if (Command == CMD_FORWARD) { //forward
    motorRun(0, 1, 1);
    motorRun(1, 0, 1);
    Serial.print("#motor  ");
    Serial.println(0);
  } else if (Command == CMD_BACKWARD) { //backward
    motorRun(0, 0, 1);
    motorRun(1, 1, 1);
    Serial.print("#motor  ");
    Serial.println(1);
  } else if (Command == CMD_LEFT) { //left
    motorRun(0, 1, 1);
    motorRun(1, 1, 1);
    Serial.print("#motor  ");
    Serial.println(2);
  } else if (Command == CMD_RIGHT) { //right
    motorRun(0, 0, 1);
    motorRun(1, 0, 1);
    Serial.print("#motor  ");
    Serial.println(3);
  } else if (Command == CMD_STOP || Command == CMD_CENTRE) { //stop
    motorRun(0, 1, 0);
    motorRun(1, 0, 0);
    Serial.print("#motor  ");
    Serial.println(4);
  } else if (Command == CMD_GATE_OPEN) {
    gateMove(1);
    Serial.print("#gate  ");
    Serial.println(1);
  } else if (Command == CMD_GATE_SHUT) {
    gateMove(0);
    Serial.print("#gate  ");
    Serial.println(0);
  } else if(Command == CMD_LED) {
    LEDcount = LED_BLINK_COUNT;
    Serial.println("#LED");
  } else if (InputString.charAt(0) == 'c') {
    int sensorIndex = parseString(InputString, ' ', 1).toInt();
    bool collision = checkCollision(sensorIndex);
    Serial.println(collision);
  }
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
<<<<<<< HEAD
  Serial.println("Y");
=======
>>>>>>> 919f42e2312135867d531b13936eb5187c7e1c38
  motorsInit();
  servoInit();
  LEDinit();  
}

void loop() {
  checkSerial();
  LEDupdate();
<<<<<<< HEAD
  
=======
  delay(1);
>>>>>>> 919f42e2312135867d531b13936eb5187c7e1c38
}
