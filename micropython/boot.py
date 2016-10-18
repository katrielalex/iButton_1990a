# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb

# main script to run after this one
pyb.main('main.py')

pyb.LED(3).on()
pyb.delay(1000)
usr_switch = pyb.Switch()()
pyb.LED(3).off()

if usr_switch:
    for _ in range(5):
        pyb.LED(3).on()
        pyb.delay(100)
        pyb.LED(3).off()
        pyb.delay(100)

    # act as a serial and a storage device
    pyb.usb_mode('VCP+MSC')
else:
    pyb.usb_mode('VCP')

# pyb.usb_mode('VCP+HID') # act as a serial device and a mouse
