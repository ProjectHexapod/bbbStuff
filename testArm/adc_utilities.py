#!/usr/bin/env python
"""
"""

from glob import glob
import logging
import os
from utilities import clamp, getPercentageIntoRange, readInt
import logging

log = logging.getLogger(__name__)

def readAin(pinName, jointRange):
  raw = readInt(pinName)
  raw = clamp(jointRange, raw)
  return getPercentageIntoRange(jointRange, float(raw))

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
ELBOW_RANGE = (1420, 3570)  # these values came from a run of calibrate.py
SHOULDER_RANGE = (845, 2736)  # these values were measured manually
# 2465
if __name__ == "__main__":
  pass
