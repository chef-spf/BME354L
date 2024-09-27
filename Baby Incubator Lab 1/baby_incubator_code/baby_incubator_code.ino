#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
// On an arduino UNO:       A4(SDA), A5(SCL)
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ 0b00000000, 0b11000000,
  0b00000001, 0b11000000,
  0b00000001, 0b11000000,
  0b00000011, 0b11100000,
  0b11110011, 0b11100000,
  0b11111110, 0b11111000,
  0b01111110, 0b11111111,
  0b00110011, 0b10011111,
  0b00011111, 0b11111100,
  0b00001101, 0b01110000,
  0b00011011, 0b10100000,
  0b00111111, 0b11100000,
  0b00111111, 0b11110000,
  0b01111100, 0b11110000,
  0b01110000, 0b01110000,
  0b00000000, 0b00110000 };

//pin variables
const int thermPin = A0;
const int controlPin = 2;
const int ledPin = 4;
const int downButtonPin = 5;
const int upButtonPin = 6;
const int buzzerPin = 10;

//steinhart-hart constants
float a = 3.354E-3;
float b = 2.570E-4;
float c = 2.620E-6;
float d = 6.383E-8;
float Rref = 10000.0;

//variables for temp control
float setTemp = 36.9;
float dangerHighTemp = 37.8;
float dangerLowTemp = 36.0;
int downButtonState = 0;
int upButtonState = 0;

void setup() {
  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  pinMode(controlPin, OUTPUT);
  digitalWrite(controlPin, LOW);
  pinMode(downButtonPin, INPUT);
  pinMode(upButtonPin, INPUT);

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();
  display.setTextSize(1);      // Set the text size (1 is default)
  display.setTextColor(SSD1306_WHITE); // White color for text
  delay(2000); // Pause for 2 seconds
}

void loop() {
  int thermAnalog = analogRead(thermPin);
  float thermVoltage = thermAnalog*(5.00/1023.0);
  float thermResistance = ((float)50e3/thermVoltage) - 10000.0;

  //Steinhart-hart eq
  float lnR = log(thermResistance/Rref);
  float T_inv = a + b*lnR + c*pow(lnR, 2.0) + d*pow(lnR, 3.0);
  float T_K = 1/T_inv;
  float T_C = T_K - 273.15;

  //temp control
  if (T_C < setTemp - 0.10) {
    digitalWrite(controlPin, HIGH);
  } else if (T_C > setTemp + 0.10) {
    digitalWrite(controlPin, LOW);
  }
  
  if (T_C > dangerHighTemp) {
    digitalWrite(ledPin, HIGH);
    tone(buzzerPin, 1000);
  } else if (T_C < dangerLowTemp) {
    digitalWrite(ledPin, HIGH);
    tone(buzzerPin, 800);
  } else {
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
  }

  downButtonState = digitalRead(downButtonPin);
  upButtonState = digitalRead(upButtonPin);
  
  if (downButtonState == HIGH) {
    setTemp = setTemp - 0.1;
  }
  if (upButtonState == HIGH) {
    setTemp = setTemp + 0.1;
  }

  // Display the voltage on the OLED
  display.clearDisplay(); // Clear previous display
  display.setCursor(0,0); // Set cursor to top-left corner
  display.print("Voltage: ");
  display.print(thermVoltage);
  display.println(" V");
  display.print("Heater Temp: ");
  display.print(T_C);
  display.println(" C");
  display.print("Set Temp: ");
  display.print(setTemp);
  display.println(" C");

  if (setTemp < dangerLowTemp) {
    display.println("DANGER: Too Low");
  }
  if (setTemp > dangerHighTemp) {
    display.println("DANGER: Too High");
  }

  display.display(); // Update the display with the new data

  //Debugging prints
  //Serial.print(thermAnalog);
  //Serial.print(", ");
  // Serial.print(thermVoltage);
  // Serial.print(", ");
  // Serial.print(thermResistance);
  // Serial.print(", ");
  // Serial.print(lnR);
  // Serial.print(" ,");
  // Serial.println(T_C);
  delay(100);
}