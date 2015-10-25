#!/usr/bin/env python
"""
"""

from time import sleep

def setDutyCycle(ns):
  with open("/sys/class/pwm/pwmchip0/pwm0/duty_cycle", mode="w") as f:
    f.write(str(ns))

def readAnalogOnce():
  sleep(.005)
  with open("/sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage2_raw") as f:
    return int(f.read())

def readAnalog():
  readings = [readAnalogOnce() for i in range(10)]
  return sum(readings) / float(len(readings))

def stopAndQuit():
  setDutyCycle(0)
  import sys
  sys.exit(0)


if __name__ == '__main__':
  import signal
  signal.signal(signal.SIGABRT, lambda a,b: stopAndQuit())
  signal.signal(signal.SIGINT, lambda a,b: stopAndQuit())
  signal.signal(signal.SIGQUIT, lambda a,b: stopAndQuit())

  for duty in range(20000):
    setDutyCycle(duty)
    sleep(.010)
    reading = readAnalog()
    dutyFraction = duty / 50000.
    print dutyFraction, reading, (14 / 1.18 * dutyFraction)
    if reading > 500:
      break
    sleep(.010)
  setDutyCycle(0)
