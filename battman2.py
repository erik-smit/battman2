import time
import parallel
import numpy as np

#define DA_RESET 0x40
#define DA_INCREMENT 0x80
#define CONNECT_RELAY 0x20
#define CHARGE_RELAY 0x10
#define RATE_MASK 0x0F
#define LOW_SENSE 0x10
#define HIGH_SENSE 0x08

#BIT_WEIGHTS   = np.array([0.0008, 0.0016, 0.0031, 0.0061, 0.009, 0.020, 0.045, 0.086, 0.180, 0.365, 0.736, 1.474])
BIT_WEIGHTS   = [0.0008, 0.0016, 0.0031, 0.0061, 0.009, 0.020, 0.045, 0.086, 0.180, 0.365, 0.736, 1.474]
VOLT_MULT     = 6.4965986394557823129251700680272
#BIT_WEIGHTS   = [1.474, 0.736, 0.365, 0.180, 0.086, 0.045, 0.020, 0.009, 0.0061, 0.0031, 0.0016, 0.0008]

DA_RESET      = 1<<6
DA_INCREMENT  = 1<<7
CONNECT_RELAY = 1<<5
CHARGE_RELAY  = 1<<4

LOW_SENSE     = 1<<4
HIGH_SENSE    = 1<<3

class Battman2(object):
    def __init__(self):
        self.p = parallel.Parallel()
        count = 0
        self.data = 0

    def pulse(self, cmd):
        self.data |= cmd
        self.p.setData(self.data)
        self.data &= ~cmd
        self.p.setData(self.data)

    def connectBattery(self):
        self.data |= CONNECT_RELAY
        self.p.setData(self.data)

    def disconnectBattery(self):
        self.data &= ~CONNECT_RELAY
        self.p.setData(self.data)

    def chargeMode(self):
        self.data |= CHARGE_RELAY
        self.p.setData(self.data)

    def dischargeMode(self):
        self.data &= ~CHARGE_RELAY
        self.p.setData(self.data)

    def readVoltage(self):
	count = 0
        lo = 0
        hi = 0
        maxCount = 1<<12
        self.pulse(DA_RESET)
        time.sleep(0.01)
        while (count<4095):
            self.pulse(DA_INCREMENT)
#            time.sleep(0.0001)
            if self.p.getInSelected(): #
		lo = self.bitsToVolt(count)
            if self.p.getInError(): #
		hi = self.bitsToVolt(count)
            count += 1
        return hi - lo

    def bitsToVolt(self, bits):
        count = 0
        result = 0
        while (count<13):
           if (bits & 1<<count):
               result += BIT_WEIGHTS[count]
           count += 1
        return result * VOLT_MULT

    def clean(self):
        self.data = 0
        self.p.setData(self.data)

    def count(self):
        while (count<8):
            self.data = 1<<count
            self.p.setData(self.data)
            time.sleep(1)
            print(self.data)
            #self.data = 0x0
            count += 1
        self.p.setData(0)




