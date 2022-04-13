#define saka 13
#define saki 11
#define duaka 12
#define duaki 10
#define tika 8
#define tiki 9
#define enb 7
#define mosaka 6
#define mosaki 5
#define moduaka 4
#define moduaki 3
#define pneumatic 2
#define ir A3

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(saka, OUTPUT);
  pinMode(saki, OUTPUT);
  pinMode(duaka, OUTPUT);
  pinMode(duaki, OUTPUT);
  pinMode(tika, OUTPUT);
  pinMode(tiki, OUTPUT);
  pinMode(enb, OUTPUT);
  pinMode(mosaka, OUTPUT);
  pinMode(mosaki, OUTPUT);
  pinMode(moduaka, OUTPUT);
  pinMode(moduaki, OUTPUT);
  pinMode(pneumatic, OUTPUT);
}

int motor1 = -100;
int motor2 = 100;
int motor3 = 0;
bool motora1 = false;
bool motora2 = false;

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(enb, HIGH);
  if (motor1 > 0) {
    digitalWrite(saka, HIGH);
    analogWrite(saki, 255 - motor1);
  }
  else if (motor1 < 0) {
    digitalWrite(saka, LOW);
    analogWrite(saki, -motor1);
  }
  if (motor2 > 0) {
    digitalWrite(duaka, HIGH);
    analogWrite(duaki, 255 - motor2);
  }
  else if (motor2 < 0) {
    digitalWrite(duaka, LOW);
    analogWrite(duaki, -motor2);
  }

  if (motor3 > 0) {
    digitalWrite(tika, LOW);
    analogWrite(tiki, motor3);
  }
  else if (motor3 < 0) {
    digitalWrite(tika, HIGH);
    analogWrite(tiki, 255 + motor3);
  }

  if (motora1) {
    digitalWrite(moduaka, LOW);
    analogWrite(moduaki, 255);
  }
  if (motora2) {
    digitalWrite(mosaka, HIGH);
    analogWrite(mosaki, 0);
  }

//  digitalWrite(pneumatic, HIGH);
  Serial.println(scanIr());
}

int scanIr() {
  float A = analogRead(ir) * 0.0048828125;
  double jarak = 65 * pow(A, -1.15);
  double B = (jarak / 1023 * 5) * 100 - 4;
  //Serial.print(B);
  return B;
}
