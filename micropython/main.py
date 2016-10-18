# main.py -- put your code here!

from machine import Pin
import pyb
import onewire
import onewireslave
import time
import os
import ubinascii

successled = pyb.LED(4)
warnled = pyb.LED(3)

shortpin = Pin('X12', mode=Pin.OUT)
shortpin.value(1)
toggleread = Pin('Y6', mode=Pin.OUT)
toggleread.value(0)
toggleread.init(Pin.IN)

if 1:
    print("Write mode")
    ows = onewireslave.OneWireSlave(Pin('Y5'), [0x01, 0x19, 0x76, 0x60, 0x09, 0x00, 0x00, 0x8e])
    ows.waitForRequest(False)
else:
    print("Read mode")
    # create a OneWire bus on GPIO12
    ow = onewire.OneWire(Pin('Y5'))

    while True:
        roms = ''
        while not roms:
            try:
                roms = ow.scan()
            except OSError as e:
                for _ in range(3):
                    warnled.on()
                    time.sleep_ms(100)
                    warnled.off()
                    time.sleep_ms(100)
                pass
            time.sleep_ms(250)

        successled.on()
        with open('ROMS', 'a') as romlog:
            romlog.write("Rom Found: {}\n".format(ubinascii.hexlify(roms[0])))
            print(os.listdir())
            romlog.flush()
        time.sleep_ms(250)
        successled.off()
        time.sleep_ms(750)
        os.sync()
        pyb.hard_reset()
