String s;
char  x;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0)
  {
    x = Serial.read();
    s += x;
    if (x == ';') {
      int commaIndex = s.indexOf(',');
      //  Search for the next comma just after the first
      int secondCommaIndex = s.indexOf(',', commaIndex + 1);

      String firstValue = s.substring(0, commaIndex);
      String secondValue = s.substring(commaIndex + 1, secondCommaIndex);
      String thirdValue = s.substring(secondCommaIndex + 1); // To the end of the string

      int r = firstValue.toInt();
      int g = secondValue.toInt();
      int b = thirdValue.toInt();

      Serial.print("r = ");
      Serial.print(r);
      Serial.print(" g = ");
      Serial.print(g);
      Serial.print(" b = ");
      Serial.println(b);
      s = "";
    }
  }
}



