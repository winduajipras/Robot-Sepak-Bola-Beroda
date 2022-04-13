#define motor1a 11  
#define motor1b 10
#define motor2a 6
#define motor2b 9
#define motor3a 5
#define motor3b 3
#define motorEn 7
#define pneumatic 2
#define ir  A4

int motor[] = {
  motor1a, motor1b, motor2a, motor2b, motor3a, motor3b, motorEn, pneumatic
};
float motor1, motor2, motor3, angular;
float rotatePWM = 0; //perlu di-PID-kan
float maxPWM = 255;
int speedRobot = 100;    //kecepatan robot mendekati bola (0-255)
int error, lastError, kp = 1, kd = 7;
int sudut, bola, tendang, radius;
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
  scanIr();
  if (Serial.available() > 0)
  {
    a = Serial.read();
    s += a;
    if (a == ';') {
      int commaIndex = s.indexOf(',');
      //  Search for the next comma just after the first
      int secondCommaIndex = s.indexOf(',', commaIndex + 1);

      String firstValue = s.substring(0, commaIndex);
      String secondValue = s.substring(commaIndex + 1, secondCommaIndex);
      String thirdValue = s.substring(secondCommaIndex + 1); // To the end of the string

      sudut = firstValue.toInt();
      bola = secondValue.toInt();
      tendang = thirdValue.toInt();

      Serial.print("sudut:");
      Serial.print(sudut);
      Serial.print("  bola:");
      Serial.print(bola);
      Serial.print("  tendang:");
      Serial.print(tendang);

      //*******************invers kinematic************************
      //menentukan nilai +- angular dan error
      if (sudut == 0) {
        error = sudut;
        angular = 0;
        lastDir = false;
      }
      else if (sudut > 0) {
        error = sudut;
        rotatePWM = pid(error);
        angular = rotatePWM / maxPWM;
        lastDir = false;
      }
      else {
        error = -sudut;
        rotatePWM = pid(error);
        angular = 0 - rotatePWM / maxPWM;
        lastDir = true;
      }

      if (bola == 0) {
        //robot berputar ke kanan
        if (!lastDir) {
          speedRobot=100;
          motor1 = speedRobot/2;
          motor2 = speedRobot/2;
          motor3 = speedRobot/2;
        }
        //robot berputar ke kiri
        else if (lastDir) {
          speedRobot=100;
          motor1 = -speedRobot/2;
          motor2 = -speedRobot/2;
          motor3 = -speedRobot/2;
        }
      }
      else {
        //rumus kontrol motor mendekati bola
        if (scanIr()<15 && tendang == 1) {
          digitalWrite(pneumatic, HIGH);
          delay(200);
          digitalWrite(pneumatic, LOW);
          delay(200);      
        

        }
        if (tendang == 1) {
          kp = 3;
          speedRobot = 50;
          motor1 = speedRobot * (cos(radians(150 - sudut)) + angular);
          motor2 = speedRobot * (cos(radians(30 - sudut)) + angular);
          motor3 = speedRobot * (cos(radians(270 - sudut)) + angular*2);
        }
        else {
          kp = 1;
          digitalWrite(motorEn, HIGH);
          speedRobot = 100;
          motor1 = speedRobot * (cos(radians(150 - sudut)) + angular);
          motor2 = speedRobot * (cos(radians(30 - sudut)) + angular);
          motor3 = speedRobot * (cos(radians(270 - sudut)) + angular*2);
        }
      }

      //limiter PWM
      if (motor1 > maxPWM)  motor1 = maxPWM;
      if (motor1 < -maxPWM) motor1 = -maxPWM;
      if (motor2 > maxPWM)  motor2 = maxPWM;
      if (motor2 < -maxPWM) motor2 = -maxPWM;
      if (motor3 > maxPWM)  motor3 = maxPWM;
      if (motor3 < -maxPWM) motor3 = -maxPWM;

      //kontrol arah motor CW (a-, b+) dan CCW (a+, b-)
      if (motor1 >= 0) {
        digitalWrite(motor1a, LOW);
        analogWrite(motor1b, motor1);
      }
      if (motor1 < 0) {
        analogWrite(motor1a, -motor1);
        digitalWrite(motor1b, LOW);
      }
      if (motor2 >= 0) {
        digitalWrite(motor2a, LOW);
        analogWrite(motor2b, motor2);
      }
      if (motor2 < 0) {
        analogWrite(motor2a, -motor2);
        digitalWrite(motor2b, LOW);
      }
      if (motor3 >= 0) {
        digitalWrite(motor3a, LOW);
        analogWrite(motor3b, motor3);
      }
      if (motor3 < 0) {
        analogWrite(motor3a, -motor3);
        digitalWrite(motor3b, LOW);
      }

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

int pid(int err) {
  if (err > 20) err = 20;
  int pid = (err * kp) + ((err - lastError) * kd);
  lastError = err;
  return pid;
}

int scanIr(){
  float A = analogRead(ir) * 0.0048828125;
  double jarak = 65 * pow(A, -1.15);
  double B = (jarak/1023*5)*100-4;
  //Serial.print(B);
  return B; 
}






