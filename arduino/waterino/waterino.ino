
#include <DHT.h>
#include <LiquidCrystal.h>
#include <Ultrasonic.h>

#define DHTPIN 6
#define DHTTYPE DHT11

// initialize the LCD library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// initialize the distance sensor for the water tank
Ultrasonic ultrasonic(7, 8);

// initialize the temp and humidity sensor
DHT dht(DHTPIN, DHTTYPE);

// Arduino pins
int moisture_sensor0 = 0; // Soil moisture input at Analog PIN A0
int moisture_sensor1 = 1; // Soil moisture input at Analog PIN A1
int light_sensor = 2; // Photoresistor
int waterpump_pin0 = 10; // Waterpump 
int waterpump_pin1 = 9; // Waterpump 

int moisture = 0;
int water_level = 0;
int old_water_level = 0;
int old_moisture = 0;
float empty_tank_reading = 32.0; // Distance in CM to the bottom of the watertank
String m = "m:"; // Soil moisture
String w = "w:"; // Tank water level
String t = "t:"; // Air temperature
String h = "h:"; // Air humidity

void setup() {
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  dht.begin();
  Serial.begin(9600);
  pinMode(waterpump_pin0, OUTPUT);
  pinMode(waterpump_pin1, OUTPUT);
  
}

int run_pump(int duration, int pin){
  lcd.setCursor(0, 1);
  lcd.print("Watering for 3 seconds!");
  Serial.println("Watering for 3 seconds!");
  digitalWrite(pin, HIGH);
  delay(duration);
  digitalWrite(pin, LOW);
}

int get_moisture_reading(int pin){
  int moisture = analogRead(pin);
  moisture = 104-moisture/10;
  return moisture;
}

int get_water_level_percentage(){
  float wl_reading = ultrasonic.distanceRead();
  float percentage = wl_reading / empty_tank_reading;
  int p = (int) percentage;
  return p;
}


void loop() {
  delay(2000);
  moisture = get_moisture_reading(moisture_sensor0);
  // Or if using two sensors:
  // int moisture = get_moisture_reading(moisture_sensor0) + get_moisture_reading(moisture_sensor1) / 2;
  water_level = get_water_level_percentage();
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  Serial.println(w + water_level);
  Serial.println(m + moisture);
  Serial.println(t + temperature);
  Serial.println(h + humidity);

  if(moisture != old_moisture){
    lcd.setCursor(0, 0);
    lcd.print("M:");
    lcd.print(moisture);
    lcd.print('%');
    old_moisture = moisture;
  }

  // if(water_level != old_water_level){
    lcd.setCursor(10, 0);
    lcd.print("WL:");
    lcd.print(water_level);
    lcd.print('%');
    old_water_level = water_level;
  //}
  
  if (Serial.available() > 0) {
    String serial_value = Serial.readString();
    if (serial_value == "go") {
      lcd.setCursor(0, 1);
      lcd.print("                  ");
      lcd.setCursor(0, 1);
      lcd.print("Manual watering!");
      delay(5000);
      Serial.println("Manual watering triggered!");
      run_pump(3000, waterpump_pin0);
    }
   }  

  if(moisture<20) {
    run_pump(3000, waterpump_pin0);
    lcd.setCursor(0, 1);
    lcd.print("                  ");
    lcd.setCursor(0, 1);
    lcd.print("Sleeping 5s...");
    moisture = get_moisture_reading(moisture_sensor0);
    // Or if using two sensors:
    // moisture = get_moisture_reading(moisture_sensor0) + get_moisture_reading(moisture_sensor1) / 2;
    int count = 0;
    while(count < 10){
      if(moisture != old_moisture){
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("M: ");
        lcd.print(moisture);
        old_moisture = moisture;
      }
      delay(500);
      moisture = get_moisture_reading(moisture_sensor0);
    // Or if using two sensors:
    // moisture = get_moisture_reading(moisture_sensor0) + get_moisture_reading(moisture_sensor1) / 2;
      count++;
      
    }
  }
}
