iButton_1990a
=============

Arduino sketch to impersonate an iButton 1990A fob. Based on [OneWireSlave](https://github.com/MarkusLange/OneWireSlave) but heavily modified. The important code is in the OneWireSlave library in lib; the sketch in src just calls its API.

Dependencies
============

* [ino](http://inotool.org/), unless you want to deal with compiling things in the Arduino GUI 
* Arduino, installed in the standard location, or passed as `ino build -d ARDUINO_DIR`
* if you don't have the standard `OneWire` library installed, run `git submodule update --init` to get a copy of bigjosh's [OneWireNoResistor](https://github.com/bigjosh/OneWireNoResistor)

Running
=======

You can set up your board to act either as a master device to read a fob, or as a fob itself.

For the former, give the compiler a `-DREADER` flag, e.g. 

	ino build -f="-DREADER"

This sets up the board as a portable reader that reads keys, stores them in EEPROM, and dumps them to serial if it receives anything over serial (to indicate the bus exists). Note that on Arduino Nanos, the pin used here (2) is adjacent to the ground pin, so you can actually tap a fob directly onto the board's pins to read it.

For the latter, add a `roms.config` file in `src` with the ID of the fob you want to impersonate. A sample file is already there, or you can read the code off of your own fob using the OneWire Library. Then build with

    ino build

Either way, upload and listen on serial with 

    ino upload && ino serial
