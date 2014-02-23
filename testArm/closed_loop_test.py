#!/usr/bin/env python
"""
"""

from pid import PIDController
from stop import stopEverythingAndQuit
import time

def readInt(filename):
  with open(filename) as f:
    return int(f.read())

PWM_PERIOD = readInt("/sys/devices/ocp.3/pwm_test_P9_22.13/period")
SENSOR_RANGE = (1420, 3570)  # these values came from a run of calibrate.py

def readAin():
  raw = readInt("/sys/bus/iio/devices/iio:device0/in_voltage3_raw")
  raw = clamp(SENSOR_RANGE, raw)
  return getPercentageIntoRange(SENSOR_RANGE, float(raw))

def getPercentageIntoRange(range, distance):
  return (distance - range[0]) / (range[1] - range[0])

def writePwm(name, val):
  with open("/sys/devices/ocp.3/pwm_test_%s/duty" % name, mode="w+") as f:
    f.write(str(val))

def clamp(limits, control):
  return min(limits[1], max(limits[0], control))

def percentageClamp(control):
  return clamp((-1., 1.), control)

def mapControlToPwmPair(control):
  control = percentageClamp(control)
  mag = 1. - abs(control)  # the 1 - here is because pwm duty 0 corresponds to full speed instead of stop
  result = mag * PWM_PERIOD * .8  + PWM_PERIOD * .2
  return (PWM_PERIOD, int(result)) if control > 0 else (int(result), PWM_PERIOD)

def executePwmPair(pair):
  print "Commanding %s" % str(pair)
  writePwm("P9_22.13", pair[0])
  writePwm("P9_21.12", pair[1])

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
  import signal
  signal.signal(signal.SIGINT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGABRT, lambda a,b: stopEverythingAndQuit())
  # signal.signal(signal.SIGKILL, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGQUIT, lambda a,b: stopEverythingAndQuit())
  main()
