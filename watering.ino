#include <LiquidCrystal.h>
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
int pump_pin = 10;
int old_moisture = 0;

int sensor = 0; // Soil Sensor input at Analog PIN A0
int moisture = 0;
void setup() {
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(pump_pin, OUTPUT);
}

int run_pump(int duration){
    digitalWrite(pump_pin, HIGH);
    delay(duration);
    digitalWrite(pump_pin, LOW);
}

int get_moisture_reading(){
  moisture = analogRead(sensor);
  moisture = moisture/10;
  return moisture;
}

void loop() {
  moisture = get_moisture_reading();
  Serial.println(moisture);
  if(moisture != old_moisture){
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Moisture: ");
    lcd.print(moisture);
    old_moisture = moisture;
  delay(500);
  }
  if(moisture>40)
  {
    lcd.setCursor(0, 1);
    lcd.print("Watering for 3 seconds!");
    run_pump(3000);
    lcd.setCursor(0, 1);
    lcd.print("                  ");
    lcd.setCursor(0, 1);
    lcd.print("Sleeping...");
    moisture = get_moisture_reading();
    int count = 0;
    while(count < 10){
      if(moisture != old_moisture){
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Moisture: ");
        lcd.print(moisture);
        old_moisture = moisture;
      }
      delay(500);
      count++;
    }
  }
}
