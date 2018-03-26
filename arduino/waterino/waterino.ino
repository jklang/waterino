#include <DHT.h>
#include <LiquidCrystal.h>
#include <Ultrasonic.h>

#define DHTPIN 6
#define DHTTYPE DHT22

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

// Initialize variables
int moisture = 0;
int water_level = 0;
float temperature = 0.0;
float humidity = 0.0;
int light_reading = 0;
int old_water_level = 0;
int old_moisture = 0;
float old_temperature = 0.0;
float old_humidity = 0.0;
int old_light_reading = 0;

String m = "m:"; // Soil moisture
String w = "w:"; // Tank water level
String t = "t:"; // Air temperature
String h = "h:"; // Air humidity
String l = "l:"; // Light

// Configure according to the size of your water tank
float empty_tank_reading = 28.0; // Distance in CM to the bottom of the water tank
float full_tank_reading = 7.0; // Distance in CM to the level of the water when the tank is considered full

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
  moisture = moisture/10;
  return moisture;
}

int get_water_level_percentage(){
  float wl_reading = ultrasonic.distanceRead();
  float wl = empty_tank_reading - wl_reading;
  float percentage = ((wl_reading - empty_tank_reading) * 100)/(full_tank_reading - empty_tank_reading);
  //float percentage = wl / empty_tank_reading * 100;
  int p = (int) percentage;
  return p;
}

void loop() {
  delay(2000);
  // Get sensor readings
  light_reading = analogRead(light_sensor); 
  moisture = get_moisture_reading(moisture_sensor0);
  // Or if using two sensors:
  // int moisture = get_moisture_reading(moisture_sensor0) + get_moisture_reading(moisture_sensor1) / 2;
  water_level = get_water_level_percentage();
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  // Print values from the sensors on the serial port
  Serial.println(w + water_level);
  Serial.println(m + moisture);
  Serial.println(t + temperature);
  Serial.println(h + humidity);
  Serial.println(l + light_reading);

  // Print moisture value on LCD
  if(moisture != old_moisture){
    lcd.setCursor(0, 0);
    lcd.print("M:");
    lcd.print(moisture);
    lcd.print('%');
    old_moisture = moisture;
  }
  // Print water level value on LCD
  if(water_level != old_water_level){
    lcd.setCursor(10
      , 0);
    lcd.print("W:");
    lcd.print(water_level);
    lcd.print('%');
    old_water_level = water_level;
  }
  // Print humidity on LCD
  if(humidity != old_humidity){
    int h = (int) humidity;
    lcd.setCursor(0, 1);
    lcd.print("H:");
    lcd.print(h);
    lcd.print('%');
    old_humidity = humidity;
  }
  // Print temperature on LCD
  if(temperature != old_temperature){
    int t = (int) temperature;
    lcd.setCursor(10, 1);
    lcd.print("T:");
    lcd.print(t);
    lcd.print((char)223);
    lcd.print("C");
    old_temperature = temperature;
  }
  
  // If there's a go received on the serial bus. Trigger manual watering
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

  if(moisture == 2000) {
    run_pump(3000, waterpump_pin0);
    lcd.setCursor(0, 1);
    lcd.print("                  ");
    lcd.setCursor(0, 1);
    lcd.print("Sleeping 10s...");
    moisture = get_moisture_reading(moisture_sensor0);
    // Or if using two sensors:
    // moisture = get_moisture_reading(moisture_sensor0) + get_moisture_reading(moisture_sensor1) / 2;
    int count = 0;
    while(count < 20){
      if(moisture != old_moisture){
        lcd.setCursor(0, 0);
        lcd.print("M: ");
        lcd.print(moisture);
        lcd.print('%');
        old_moisture = moisture;
      if(water_level != old_water_level){
        lcd.setCursor(9, 0);
        lcd.print("WL:");
        lcd.print(water_level);
        lcd.print('%');
        old_water_level = water_level;
      }
        
      }
      delay(500);
      moisture = get_moisture_reading(moisture_sensor0);
    // Or if using two sensors:
    // moisture = get_moisture_reading(moisture_sensor0) + get_moisture_reading(moisture_sensor1) / 2;
      count++;
      
    }
  }
}
