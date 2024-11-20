#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128  // OLED display width, in pixels
#define SCREEN_HEIGHT 64  // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library.
// On an arduino UNO:       A4(SDA), A5(SCL)
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define NUMFLAKES 10  // Number of snowflakes in the animation example

#define LOGO_HEIGHT 16
#define LOGO_WIDTH 16
static const unsigned char PROGMEM logo_bmp[] = { 0b00000000, 0b11000000,
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

//________________________________________________________________________
constexpr int k = 12;
constexpr int sampleSize = 2 * k;
int sampleWindow[sampleSize + 1] = { 0 };
int indexFill = 0;


int peak = 0;
int wait = 0;
constexpr int HRWindowSize = 6;
int HRWindow[HRWindowSize] = { 0 };


unsigned long timeofPeak;
unsigned long lastPeak = 0;
unsigned long interval;


//_________________________________________________________________________

void setup() {
  Serial.begin(9600);  // Serial connection to print samples
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;  // Don't proceed, loop forever
  }
  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000);  // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();
  display.setTextSize(1);               // Set the text size (1 is default)
  display.setTextColor(SSD1306_WHITE);  // White color for text
  delay(2000);                          // Pause for 2 seconds
}

void loop() {
  // Creation of a window array, that takes new data in and throws old data out in real-time
  int currentVal = analogRead(A0);
  for (int i = 0; i < sampleSize; i++) {
    sampleWindow[i] = sampleWindow[i + 1];
  }
  sampleWindow[sampleSize] = currentVal;

  if (indexFill < sampleSize) {
    indexFill++;
  }

  if (indexFill == sampleSize) {
    float leftAvg = calculateAvg("left");
    float rightAvg = calculateAvg("right");
    float totAvg = (leftAvg + rightAvg) / 2.0;

    if (wait <= 0 && sampleWindow[k] > leftAvg && sampleWindow[k] > rightAvg && sampleWindow[k] > totAvg * 1.2) {
      //Signal a peak
      peak = 1000;
      //Record time of peak
      timeofPeak = millis();
      //Implement refractory period to prevent the detection of another peak.
      wait = 25;

      //Calculate HR based on the time from the last detected peak to the current detected peak
      if (lastPeak != 0) {
        interval = timeofPeak - lastPeak;
        int HR = round(60000 / interval);
        // Display the voltage on the OLED
        for (int i = 0; i < HRWindowSize - 1; i++) {
          HRWindow[i] = HRWindow[i + 1];
        }
        HRWindow[HRWindowSize - 1] = HR;
        int HRAverage = round(calculateHRAvg());


        // int count = sizeof(HRWindow) / sizeof(HRWindow[0]);
        // printArray(HRWindow, count);


        display.clearDisplay();   // Clear previous display
        display.setCursor(0, 0);  // Set cursor to top-left corner
        display.print("Instantaneous HR: ");
        display.print(HR);
        display.println(" BPM");
        display.print("Average HR: ");
        display.print(HRAverage);
        display.println(" BPM");
        display.display();
      }
      lastPeak = timeofPeak;
    } else {
      peak = 0;
    }
  }

  wait = wait - 1;

  //Constant value to keep the scale of the serial display constant
  int constant = 1000;
  // Print values
  Serial.print(currentVal);
  Serial.print(", ");
  Serial.print(constant);
  Serial.print(", ");
  Serial.println(peak);
  delay(10);
}

//_____________________________________________________________________

//Function to calculate average
float calculateAvg(String side) {
  float sum = 0;
  if (side == "left") {
    for (int i = 1; i < k; i++) {
      sum += sampleWindow[k - i];
    }
  } else if (side == "right") {
    for (int i = 1; i < k; i++) {
      sum += sampleWindow[k + i];
    }
  }
  return sum / k;
}

// Function to calculate the average HR from an array of HR values
int calculateHRAvg() {
  int sum = 0;
  for (int i = 0; i < HRWindowSize - 1; i++) {
    sum += HRWindow[i];
  }
  return float(sum / HRWindowSize);
}

void printArray(int arr[], int size) {
  Serial.print("{");
  for (int i = 0; i < size; i++) {
    Serial.print(arr[i]);
    if (i < size - 1) {
      Serial.print(", ");
    }
  }
  Serial.println("}");
}
