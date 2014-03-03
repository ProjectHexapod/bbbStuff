#!/usr/bin/env python
"""
"""

from glob import glob
import logging
import os

log = logging.getLogger(__name__)

def readInt(filename):
  # TODO: catch IO error  (errno 11)
  with open(filename) as f:
    return int(f.read())

def clamp(limits, control):
  return min(limits[1], max(limits[0], control))

def readAin(pinName):
  raw = readInt(pinName)
  raw = clamp(SENSOR_RANGE, raw)
  return getPercentageIntoRange(SENSOR_RANGE, float(raw))

def getPercentageIntoRange(range, distance):
  return (distance - range[0]) / (range[1] - range[0])

def setupSignalHandlers():
  import signal
  from pwm_utilities import stopEverythingAndQuit
  signal.signal(signal.SIGABRT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGINT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGQUIT, lambda a,b: stopEverythingAndQuit())

def getAinPinName(pin):
  hits = glob("/sys/bus/iio/devices/iio:device?/in_voltage%s_raw" % pin)
  if hits:
    return hits[0]
  else:
    log.fatal("Could not find ADC pin %s, double check that the firmware loaded..." % pin)
    from pwm_utilities import stopEverythingAndQuit
    stopEverythingAndQuit()

AIN3 = getAinPinName(3)
AIN5 = getAinPinName(5)
SENSOR_RANGE = (1420, 3570)  # these values came from a run of calibrate.py

if __name__ == "__main__":
  pass
