#!/usr/bin/env python
"""
"""

from pid import PIDController
from pwm_utilities import stopEverythingAndQuit
import time
from utilties import *


def writePwm(name, val):
  with open("/sys/devices/ocp.3/pwm_test_%s/duty" % name, mode="w+") as f:
    f.write(str(val))

def percentageClamp(control):
  return clamp((-1., 1.), control)

def mapControlToPwmPair(control):
  control = percentageClamp(control)
  mag = 1. - abs(control)  # the 1 - here is because pwm duty 0 corresponds to full speed instead of stop
  result = mag * PWM_PERIOD * .8  + PWM_PERIOD * .2  # this is too naive
  return (PWM_PERIOD, int(result)) if control > 0 else (int(result), PWM_PERIOD)

def executePwmPair(pair):
  print "Commanding %s" % str(pair)
  writePwm("P9_22.13", pair[0])
  writePwm("P9_14.14", utilities.PWM_PERIOD - pair[0])  # LED
  writePwm("P9_21.12", pair[1])
  writePwm("P9_16.15", utilities.PWM_PERIOD - pair[1])  # LED

def main():
  pid = PIDController(1., 0, .1)
  lastTime = time.time()
  while True:
    reading = readAin()
    print "Read: %s" % reading
    now = time.time()
    control = pid.update(.5, reading, now - lastTime)
    pair = mapControlToPwmPair(control)
    executePwmPair(pair)
    lastTime = now
    time.sleep(.1)  # because the valve response rate is 10Hz



if __name__ == "__main__":
  setupSignalHandlers()
  try:
    main()
  except:
    pass  # no matter what everything should stop, so catch everything
  stopEverythingAndQuit()
