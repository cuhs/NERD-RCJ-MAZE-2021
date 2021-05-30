#ifndef _global_vars_h_
#define _global_vars_h_

#include <MeMegaPi.h>
#include <Arduino.h>
//#include <Servo.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

extern "C" {
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}
#include "Adafruit_VL53L0X.h"
#include "Adafruit_TCS34725.h"

// Function prototypes
void doTurn(char dir, int deg);
void goForward(int dist);
void goForwardTiles(int tiles);
void getDist(int start);
void motorControl();
void sendWallValues(int leftDist, int rightDist, int frontDist);
void tcaselect(uint8_t i);
void setupSensors();
int getSensorReadings(int sensorNum);
void alignLeft();
void alignRight();
void alignFront();
void alignRobot();

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);
VL53L0X_RangingMeasurementData_t measure;

// I2C address of MUX
#define TCAADDR 0x70

class MegaPiPort: public MeMegaPiDCMotor {
  public:
    bool  backwards;
    volatile uint8_t port;
    volatile uint8_t intPin;
    volatile uint8_t NEPin;
    volatile long    count;
    volatile int16_t  speed;
    MegaPiPort(uint8_t p, uint8_t i, uint8_t n): MeMegaPiDCMotor(p), port(p), intPin(i), NEPin(n), backwards(false) { };
    inline void run(int16_t s) {
      int ts = (backwards) ? -s : s;
      MeMegaPiDCMotor::run(ts);
      speed = s;
    };
    inline void reverse() {
      speed = -speed;
      run(speed);
    };
    inline void changespeed(int x) {
      run (speed + x);
    }
    inline void resetcount() {
      count = 0;
    }
};

// ports[0] = port1 on the board
volatile  MegaPiPort ports[] = { {PORT1B, 18, 31},
  {PORT2B, 19, 38},
  {PORT3B, 3, 49},
  {PORT4B, 2, A1}
};

// macro to attach the interrupt to the port  (remember index = port-1 so port1 has an index of 0
#define INIT_INTERRUPT(index)   attachInterrupt(digitalPinToInterrupt(ports[index].intPin), motorinterrupt<index>, RISING)

#define LEFT 1
#define RIGHT 0

// For Turns and Movement
float WB = 23.285;
float D = 6.45;

// For Serial Communication
char message[4] = {'a', 'a', 'a', 'a'};

// For Servo
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
//int pos = 0;    // variable to store the servo position
bool shouldRun = true;
int ct = 0;

#endif
