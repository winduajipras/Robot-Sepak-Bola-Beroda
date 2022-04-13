#define motor1a 3
#define motor1b 5
#define motor2a 6
#define motor2b 9
#define motor3a 10
#define motor3b 11

int motor[] = {motor1a, motor1b, motor2a, motor2b, motor3a, motor3b};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < sizeof(motor) / 2; i++) {
    pinMode(motor[i], OUTPUT);
  }
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
}

void loop() {
  digitalWrite(motor1b, LOW);
  analogWrite(motor1a, 100);
  digitalWrite(motor2a, LOW);
  analogWrite(motor2b, 100);
  digitalWrite(motor3b, LOW);
  analogWrite(motor3a, 100);
}

