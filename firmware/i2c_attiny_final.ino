#include <Wire.h>

#define I2C_SLAVE_ADDR     0x26            // i2c slave address (38)

#define IN1                9
#define IN2_PWM            7
#define IN3_PWM            8
#define IN4                0
#define EN12               10
#define EN34               1
#define ANALOG_PIN         2
#define RESET              11

#define DATA_LEN           5
unsigned char data[DATA_LEN] = {0,0,0,0};

void setup() {

  pinMode(IN1, OUTPUT);
  pinMode(IN2_PWM, OUTPUT);
  pinMode(IN3_PWM, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(EN12, OUTPUT);
  pinMode(EN34, OUTPUT);
  
  pinMode(RESET, OUTPUT); // hopefully prevent random resets
  pinMode(ANALOG_PIN, INPUT);
  analogReference(INTERNAL1V1);

  Wire.begin(I2C_SLAVE_ADDR);      // init I2C Slave mode
  Wire.onRequest(requestEvent); // register event
  Wire.onReceive(receiveEvent);

  
}

void loop() {
  delay(100); 
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void requestEvent()
{
  int val = analogRead(ANALOG_PIN); // read from 0 to Vin
  data[3] = val;
  data[4] = val>>8;
  Wire.write(data, DATA_LEN);
}


void receiveEvent(int numBytes) {

  if(numBytes == 3) {
  data[0] = Wire.read();
  data[1] = Wire.read();
  data[2] = Wire.read();

  analogWrite(IN2_PWM, data[0]);
  analogWrite(IN3_PWM, data[1]);
  digitalWrite(IN1,  (data[2] >> 0) & 1); // 0b0001
  digitalWrite(IN4,  (data[2] >> 1) & 1); // 0b0010
  digitalWrite(EN12, (data[2] >> 2) & 1); // 0b0100
  digitalWrite(EN34, (data[2] >> 3) & 1); // 0b1000
  
  }
}



