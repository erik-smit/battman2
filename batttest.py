import battman2
import time

bt = battman2.Battman2()

bt.connectBattery()
#time.sleep(1)
#bt.disconnectBattery()
#time.sleep(1)
bt.chargeMode()
print bt.readVoltage()
print bt.readVoltage()
print bt.readVoltage()
print bt.readVoltage()
print bt.readVoltage()
#
time.sleep(1)
bt.dischargeMode()
bt.disconnectBattery()
