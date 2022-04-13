#include <Wire.h>
#include <HMC5883L.h>

HMC5883L compass;

#define motor1a 13
#define motor1b 11 //PWM
#define motor2a 12
#define motor2b 10 //PWM
#define motor3a 8
#define motor3b 9  //PWM
#define motor4a 6
#define motor4b 5  //PWM
#define motor5a 4
#define motor5b 3  //PWM
#define motorEn 7
#define pneumatic 2
#define ir  A2

int motor[] = {
  motor1a, motor1b, motor2a, motor2b, motor3a, motor3b, motor4a, motor4b, motor5a, motor5b, motorEn, pneumatic
};
float motor1, motor2, motor3, motor4, motor5, angular, hDeg, decAngle, heading;
float rotatePWM = 0; //perlu di-PID-kan
float maxPWM = 255;
int speedRobot = 100;    //kecepatan robot mendekati bola (0-255)
int error, lastError, kp = 1, kd = 7;
int sudutBola, bola, siapTendang, sudutGawang, gawang, tendang;
long timeNow;
boolean lastDir; //true = kanan, false = kiri

String s;
char a;

void setup() {
  putarKiri();
  Serial.begin(9600);
  for (int i = 0; i < sizeof(motor) / 2; i++) {
    pinMode(motor[i], OUTPUT);
  }
  digitalWrite(motorEn, HIGH);
  // Set measurement range
  compass.setRange(HMC5883L_RANGE_1_3GA);
  // Set measurement mode
  compass.setMeasurementMode(HMC5883L_CONTINOUS);
  // Set data rate
  compass.setDataRate(HMC5883L_DATARATE_30HZ);
  // Set number of samples averaged
  compass.setSamples(HMC5883L_SAMPLES_8);
  // Set calibration offset. See HMC5883L_calibration.ino
  compass.setOffset(0, 0);
}

void loop() {
  if (Serial.available() > 0)
  {
    a = Serial.read();
    s += a;
    if (a == ';') {
      parsingData();
      //*******************invers kinematic************************
      //menentukan nilai +- angular dan error
      if (sudutBola == 0) {
        error = sudutBola;
        angular = 0;
        lastDir = false;
      }
      else if (sudutBola > 0) {
        error = sudutBola;
        rotatePWM = pid(error);
        angular = rotatePWM / maxPWM;
        lastDir = false;
      }
      else {
        error = -sudutBola;
        rotatePWM = pid(error);
        angular = 0 - rotatePWM / maxPWM;
        lastDir = true;
      }

      if (bola == 0) { //jika tidak mendeteksi bola
        //robot berputar ke kanan
        if (!lastDir) {
          putarKanan();
        }
        //robot berputar ke kiri
        else if (lastDir) {
          putarKiri();
        }
      }
      else {  //jika mendeteksi bola
        if (siapTendang == 1 && scanIr() < 15) {
          //kompas();
         //Serial.print(hDeg);
          putarKiri();
          handlingKanan();
          pembatasPwmMotor();
          kontrolArahMotor();
          delay(2000);
          shoot();
          delay(500);
        }
        else {
          inversKinematic(1);
        }
      }

      pembatasPwmMotor();
      kontrolArahMotor();

      Serial.print("\tM1= ");
      Serial.print(motor1);
      Serial.print("\t");
      Serial.print("M2= ");
      Serial.print(motor2);
      Serial.print("\t");
      Serial.print("M3= ");
      Serial.println(motor3);
      s = "";
    }
  }
}

//========================FUNGSI -FUNGSI=========================

void pembatasPwmMotor() {
  //limiter PWM
  if (motor1 > maxPWM)  motor1 = maxPWM;
  if (motor1 < -maxPWM) motor1 = -maxPWM;
  if (motor2 > maxPWM)  motor2 = maxPWM;
  if (motor2 < -maxPWM) motor2 = -maxPWM;
  if (motor3 > maxPWM)  motor3 = maxPWM;
  if (motor3 < -maxPWM) motor3 = -maxPWM;
  if (motor4 > maxPWM)  motor4 = maxPWM;
  if (motor4 < -maxPWM) motor4 = -maxPWM;
  if (motor5 > maxPWM)  motor5 = maxPWM;
  if (motor5 < -maxPWM) motor5 = -maxPWM;
}

void kontrolArahMotor() {
  //kontrol arah motor CW (a-, b+) dan CCW (a+, b-)
  if (motor1 >= 0) {
    digitalWrite(motor1a, HIGH);
    analogWrite(motor1b, maxPWM - motor1);
  }
  if (motor1 < 0) {
    digitalWrite(motor1a, LOW);
    analogWrite(motor1b, -motor1);
  }
  if (motor2 >= 0) {
    digitalWrite(motor2a, HIGH);
    analogWrite(motor2b, maxPWM - motor2);
  }
  if (motor2 < 0) {
    digitalWrite(motor2a, LOW);
    analogWrite(motor2b, -motor2);
  }
  if (motor3 >= 0) {
    digitalWrite(motor3a, LOW);
    analogWrite(motor3b, motor3);
  }
  if (motor3 < 0) {
    digitalWrite(motor3a, HIGH);
    analogWrite(motor3b, maxPWM + motor3);
  }
  if (motor4 >= 0) {
    digitalWrite(motor4a, HIGH);
    analogWrite(motor4b, maxPWM - motor4);
  }
  if (motor4 < 0) {
    digitalWrite(motor4a, LOW);
    analogWrite(motor4b, -motor4);
  }
  if (motor5 >= 0) {
    digitalWrite(motor5a, HIGH);
    analogWrite(motor5b, maxPWM - motor5);
  }
  if (motor5 < 0) {
    digitalWrite(motor5a, LOW);
    analogWrite(motor5b, -motor5);
  }
}
void kompas(){
  Vector norm = compass.readNormalize();
  // Calculate heading
  heading = atan2(norm.YAxis, norm.XAxis);
  // Formula: (deg + (min / 60.0)) / (180 / PI);
  decAngle = (4.0 + (26.0 / 60.0)) / (180 / PI);
  heading += decAngle;

  // Correct for heading < 0deg and heading > 360deg
  if (heading < 0)
  {
    heading += 2 * PI;
  }

  if (heading > 2 * PI)
  {
    heading -= 2 * PI;
  }

  // Convert to degrees
  hDeg = heading * 180/PI; // mengubah rads ke derajad
  Serial.print("\tSudut = ");
  Serial.print(hDeg);
  Serial.println(" ");
  delay(100);
}

int pid(int err) {
  if (err > 20) err = 20;
  int pid = (err * kp) + ((err - lastError) * kd);
  lastError = err;
  return pid;
}

int scanIr() {
  float A = analogRead(ir) * 0.0048828125;
  double jarak = 65 * pow(A, -1.15);
  double B = (jarak / 1023 * 5) * 100 - 4;
  //Serial.print(B);
  return B;
}

void parsingData() {
  int commaIndex = s.indexOf(',');
  int secondCommaIndex = s.indexOf(',', commaIndex + 1);

  String firstValue = s.substring(0, commaIndex);
  String secondValue = s.substring(commaIndex + 1, secondCommaIndex);
  String thirdValue = s.substring(secondCommaIndex + 1);

  sudutBola = firstValue.toInt();
  bola = secondValue.toInt();
  siapTendang = thirdValue.toInt();

  Serial.print("sudutBola:");
  Serial.print(sudutBola);
  Serial.print("  bola:");
  Serial.print(bola);
  Serial.print("  siaptendang:");
  Serial.print(siapTendang);
}

void putarKanan() {
  motor1 = -speedRobot / 2;
  motor2 = -speedRobot / 2;
  motor3 = -speedRobot / 2;
}

void putarKiri() {
  motor1 = speedRobot / 2;
  motor2 = speedRobot / 2;
  motor3 = speedRobot / 2;
}

void handlingKanan() {
  motor5 = -255;
}

void handlingKiri() {
  motor4 = 255;
}

void stopHandling() {
  motor4 = 0;
  motor5 = 0;
}

void inversKinematic(int mode) {
  if (mode == 1) {
    motor1 = speedRobot * (cos(radians(150 - sudutBola)) + angular);
    motor2 = speedRobot * (cos(radians(30 - sudutBola)) + angular);
    motor3 = speedRobot * (cos(radians(270 - sudutBola)) + angular * 2);
  }
  else if (mode == 2) {
    motor1 = speedRobot * (cos(radians(150 - sudutGawang)) + angular);
    motor2 = speedRobot * (cos(radians(30 - sudutGawang)) + angular);
    motor3 = speedRobot * (cos(radians(270 - sudutGawang)) + angular * 2);
  }
}

void shoot(){
  stopHandling();
  motor1 = 0;
  motor2 = 0;
  motor3 = 0;
  pembatasPwmMotor();
  kontrolArahMotor();
  delay(500);
  digitalWrite(pneumatic, HIGH);
  delay(200);
  digitalWrite(pneumatic, LOW);
  delay(200);
}






