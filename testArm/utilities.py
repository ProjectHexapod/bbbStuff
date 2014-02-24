#!/usr/bin/env python
"""
"""

def readInt(filename):
  with open(filename) as f:
    return int(f.read())

PWM_PERIOD = readInt("/sys/devices/ocp.3/pwm_test_P9_22.13/period")
SENSOR_RANGE = (1420, 3570)  # these values came from a run of calibrate.py

def clamp(limits, control):
  return min(limits[1], max(limits[0], control))

def readAin():
  raw = readInt("/sys/bus/iio/devices/iio:device0/in_voltage3_raw")
  raw = clamp(SENSOR_RANGE, raw)
  return getPercentageIntoRange(SENSOR_RANGE, float(raw))

def getPercentageIntoRange(range, distance):
  return (distance - range[0]) / (range[1] - range[0])

def setupSignalHandlers():
  import signal
  from stop import stopEverythingAndQuit
  signal.signal(signal.SIGABRT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGINT, lambda a,b: stopEverythingAndQuit())
  # signal.signal(signal.SIGKILL, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGQUIT, lambda a,b: stopEverythingAndQuit())

if __name__ == "__main__":
  pass
