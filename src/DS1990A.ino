#include "OneWireSlave.h"
#include "roms.config"

OneWireSlave ds(2);

void setup() {
  ds.setRom(therom);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println("Begin!");
  digitalWrite(13, LOW);
  ds.waitForRequest(false);
}
