import machine
import time


class OneWireSlave:
    def __init__(self, pin, rom):
        self.pin = pin
        self.rom = rom
        self.retry_usec = 200
        self.err = ''

        self.cache = (pin.init, pin.value, pin.OUT_OD, pin.IN, pin.PULL_NONE)

        pin.init(self.pin.IN)

    def waitForRequest(self, ignore_errors):
        self.err = ''
        while 1:
            print(self.err)
            self.err = ''
            if not self.awaitReset():
                continue
            # self.waitForRequestfake(False)
            if self.recvAndProcessCmd():
                # pyb.enable_irq(i)
                return True
            if (not self.err or ignore_errors):
                continue
            else:
                print("Error: {}".format(self.err))
        # pyb.enable_irq(i)

    def recvAndProcessCmd(self):
        # self.waitForRequestfake(False)
        r = self.recv()
        if r == 0x33:
            if not self.sendData(self.rom):
                return False
            return True
        else:
            print("Received: {}".format(r))
        self.err = 'Did not receive 0x33'
        time.sleep_us(1000000)
        return False

    def awaitReset(self):
        try:
            try:
                machine.time_pulse_us(self.pin, 1)
            except:
                self.err = 'Not Connected'
                return False
            t = machine.time_pulse_us(self.pin, 0)
            if t < 480:
                self.err = 'Very short reset ' + str(t) + 'us'
                return False
        except:
            self.err = 'Very long reset'
            return False
        self.pin.init(self.pin.OUT_OD)
        self.pin.low()
        time.sleep_us(60)
        # let it float
        self.pin.init(self.pin.IN, self.pin.PULL_NONE)
        time.sleep_us(5)
        if self.pin.value() == 0:
                self.err = 'No presence response from door'
                return False
        else:
                return True

    def sendData(self, data):
        sending_byte = 0
        for sending_byte in range(8):
            self.send(data[sending_byte])
            if self.err:
                break
        return sending_byte

    def send(self, byte):
        bitmask = 1
        while (bitmask < 256) and not self.err:
            self.sendBit(1 if (bitmask & byte) else 0)
            bitmask <<= 1

    def sendBit(self, bit):
        try:
            machine.time_pulse_us(self.pin, 0, timeout_us=60)
        except:
            self.err = 'Write timeslot timeout'
            return

        if bit & 1:
            return
        else:
            self.pin.low()
            self.pin.init(self.pin.OUT_OD)
            time.sleep_us(60)
            self.pin.init(self.pin.IN, self.pin.PULL_NONE)
        return

    def recv(self):
        "Receive eight bits, by calling recvBit eight times and accumulating."
        bitmask = 1
        received = 0
        while (bitmask < 256) and not self.err:
            if(self.recvBit()):
                received |= bitmask
            bitmask <<= 1
        return received

    def recvBit(self):
        """Receive one bit

        High means 1 and low means 0. There will always be a short high pulse at the start of a time
        window, and then either it will fall (0) or not (1).
        """
        try:
            t = machine.time_pulse_us(self.pin, 0, timeout_us=100)
            if t > 30:
                return 0
            else:
                return 1
        except OSError:
            # We hit one of the two timeouts, which means it didn't go high,
            # which means a zero.
            return 0
