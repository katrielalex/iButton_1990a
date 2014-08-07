#include <OneWire.h>
#include <EEPROM.h>

// This is the pin with the 1-Wire bus on it
OneWire ds(PIN_D0);

// unique serial number read from the key
byte addr[8];

// poll delay (I think 750ms is a magic number for iButton)
int del = 1000;

// Teensy 2.0 has an LED on port 11
int ledpin = 11;

// number of values stored in EEPROM
byte n = 0;

void setup() {
  Serial.begin(9600);
  
  // wait for serial
  pinMode(ledpin, OUTPUT);
  digitalWrite(ledpin, HIGH);
  while (!Serial.dtr()) {};
  digitalWrite(ledpin, LOW);
  
  // Dump EEPROM to serial
  n = EEPROM.read(0);
  Serial.print(n, DEC); Serial.println(" keys stored:");
  
  int i, j;
  for(i=0; i<n; i++) {
    for(j=0; j<8; j++) {
      Serial.print(EEPROM.read(1 + (8 * i) + j), HEX);
      Serial.print(" ");
    }
    Serial.println("");
  }
}

void loop() {
  byte result;
  
  // search looks through all devices on the bus
  ds.reset_search();
  
  if(result = !ds.search(addr)) {
    // Serial.println("Scanning...");
  } else if(OneWire::crc8(addr, 7) != addr[7]) {
    Serial.println("Invalid CRC");
    delay(del);
    return;
  } else {
    EEPROM.write(0, n++);
    Serial.print("Storing key "); Serial.println(n, DEC);
    for(byte i=0; i<8; i++) {
      Serial.print(addr[i], HEX);
      EEPROM.write(1 + (8 * n) + i, addr[i]);
      Serial.print(" ");
    }
    Serial.print("\n");
    digitalWrite(ledpin, HIGH);
    delay(1000);
    digitalWrite(ledpin, LOW);
  }
  
  delay(del);
  return;
}

















