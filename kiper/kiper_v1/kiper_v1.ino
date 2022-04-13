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
#define ir  A3

int motor[] = {
  motor1a, motor1b, motor2a, motor2b, motor3a, motor3b, motor4a, motor4b, motor5a, motor5b, motorEn, pneumatic
};
float motor1, motor2, motor3, motor4, motor5, angular;
float rotatePWM = 0; //perlu di-PID-kan
float maxPWM = 255;
int speedRobot = 60;    //kecepatan robot mendekati bola (0-255)
int sudut, lastSudut;
int error, lastError, kp = 7, kd = 10, kr = 20;
int sudutBola, bola, siapTendang, sudutGawang, radius;
long timeNow;
boolean lastDir; //true = kanan, false = kiri

String s;
char a;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < sizeof(motor) / 2; i++) {
    pinMode(motor[i], OUTPUT);
  }
  digitalWrite(motorEn, HIGH);
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
      if (sudutBola >= 0) {
        sudut = 90;
        lastDir = false;
      }
      else {
        sudut = -90;
        sudutBola = -sudutBola;
        lastDir = true;
      }
      error = sudutBola;
      speedRobot = pid(error, radius); 
      if (sudutBola > 25 || sudutBola <-25) speedRobot = 0;     

      if (bola == 0) { //jika tidak mendeteksi bola
        //robot berputar ke kanan
        if (!lastDir) {
          //putarKanan();
        }
        //robot berputar ke kiri
        else if (lastDir) {
          //putarKiri();
        }
        motor1 = 0;
        motor2 = 0;
        motor3 = 0;
      }
      else {  //jika mendeteksi bola
        if (siapTendang == 1 && scanIr() < 15) {
//          digitalWrite(pneumatic, HIGH);
//          delay(200);
//          digitalWrite(pneumatic, LOW);
//          delay(200);
        }
        else {
          inversKinematic();
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

int pid(int err, int rad) {
  if (err > 20) err = 20;
  if (err < -20) err = -20;
  int pid = (err * kp) + ((err - lastError) * kd);
  lastError = err;
  pid = pid - (rad/70*kr);
  if (pid < 50) pid = 0;
  Serial.print(" ");
  Serial.print(pid);
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
  int thirdCommaIndex = s.indexOf(',', secondCommaIndex + 1);

  String firstValue = s.substring(0, commaIndex);
  String secondValue = s.substring(commaIndex + 1, secondCommaIndex);
  String thirdValue = s.substring(secondCommaIndex + 1, thirdCommaIndex);
  String fourthValue = s.substring(thirdCommaIndex + 1);
  
  sudutBola = firstValue.toInt();
  bola = secondValue.toInt();
  siapTendang = thirdValue.toInt();
  radius = fourthValue.toInt();

  Serial.print("sudutBola:");
  Serial.print(sudutBola);
  Serial.print("  bola:");
  Serial.print(bola);
  Serial.print("  siaptendang:");
  Serial.print(siapTendang);
  Serial.print("  radius:");
  Serial.print(radius);
}

void putarKanan() {
  motor1 = speedRobot / 2;
  motor2 = speedRobot / 2;
  motor3 = speedRobot / 2;
}

void putarKiri() {
  motor1 = -speedRobot / 2;
  motor2 = -speedRobot / 2;
  motor3 = -speedRobot / 2;
}

void handlingKiri() {
  digitalWrite(motor5a, HIGH);
  analogWrite(motor5b, 0);
}

void handlingKanan() {
  digitalWrite(motor4a, LOW);
  analogWrite(motor4b, 255);
}

void stopHandling() {
  digitalWrite(motor4b, LOW);
  digitalWrite(motor5b, LOW);
}

void inversKinematic() {
  motor1 = speedRobot * (cos(radians(150 - sudut)));
  motor2 = speedRobot * (cos(radians(30 - sudut)));
  motor3 = speedRobot * (cos(radians(270 - sudut)));
}

