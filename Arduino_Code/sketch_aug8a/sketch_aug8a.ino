char val;
#define led1 13

void setup()
{
Serial.begin(9600);
pinMode(led1, OUTPUT);
}

void loop()
{

//digitalWrite(led1,HIGH);
if (Serial.available())
{
  val = Serial.read();
  if (val == 'B')
  digitalWrite(led1,HIGH);
  else if (val == 'b')
  digitalWrite(led1,LOW);
}

}
