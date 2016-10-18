#ifdef READER
#include <OneWire.h>
#include <EEPROM.h>

// Maximum addresses we can store in eeprom
#define EEPROM_MAX 127

int ledpin = 13;
OneWire ds(2);

#if defined (__AVR_AT90USB1286__) && defined (CORE_TEENSY)
// This is the pin with the 1-Wire bus on it
OneWire ds(PIN_D0);
// Teensy 2.0 has an LED on port 11
ledpin = 11;
#endif

// unique serial number read from the key
byte addr[8];

// poll delay (I think 750ms is a magic number for iButton)
int del = 1000;

// number of values stored in EEPROM
byte n = 0;

void setup() {
	Serial.begin(9600);
	n = EEPROM.read(0);
	
	pinMode(ledpin, OUTPUT);
	digitalWrite(ledpin, LOW);
}

void loop() {
	byte result;

	// search looks through all devices on the bus
	ds.reset_search();

	if(result = !ds.search(addr)) {
		Serial.println("Scanning...");
	} else if(OneWire::crc8(addr, 7) != addr[7]) {
		Serial.println("Invalid CRC");
		delay(del);
		return;
	} else {
		if(n <= EEPROM_MAX) {
			EEPROM.write(0, n+1);
			Serial.print("Storing key "); Serial.println(n, DEC);
			for(byte i=0; i<8; i++) {
				Serial.print(addr[i], HEX);
				EEPROM.write(1 + (8 * n) + i, addr[i]);
				Serial.print(" ");
			}
			n++;
			Serial.println("");
			digitalWrite(ledpin, HIGH);
			delay(1000);
			digitalWrite(ledpin, LOW);
		} else {
			digitalWrite(ledpin, HIGH);
		}
	}

	delay(del);
	// check if there's anything on the serial buffer indicating we can dump
	if(Serial.available()) {
		Serial.println("Input on Serial buffer");
		if(n > 0) {
			dumpEEPROM();
		} else {
			while(Serial.read() != -1) {}
		}
	}
	return;
}

void dumpEEPROM() {
	// Dump EEPROM to serial
	Serial.print(n, DEC); Serial.println(" keys stored:");

	int i, j;
	for(i=0; i<n; i++) {
		for(j=0; j<8; j++) {
			Serial.print(EEPROM.read(1 + (8 * i) + j), HEX);
			Serial.print(" ");
		}
		Serial.println("");
	}


	//Reset key count if serial was 'r'
	if(Serial.read() == 'r') {
		Serial.println("Resetting keys");
		EEPROM.write(0,0);
		n = 0;
	}

	//Flush Serial
	while(Serial.read() != -1) {}
}
#endif
