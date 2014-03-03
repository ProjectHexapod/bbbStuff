#!/usr/bin/env python
"""
"""

from glob import glob
import logging
import os
from utilities import readInt

log = logging.getLogger(__name__)

def writePwm(name, val):
  # TODO: this can throw exceptions (in theory), make sure they're dealt with nicely
  with open(name, mode="w+") as f:
    f.write(str(val))

def stop(*pins):
  for pin in pins:
    if hasattr(pin, "__iter__"):
      for p in pin:
        stop(p)
    elif pin == GREEN_LED or pin == BLUE_LED:
      writePwm(pin, 0)
    else:
      writePwm(pin, PWM_PERIOD)

def stopEverything():
  stop(GREEN_LED, BLUE_LED, P8_13, P8_19, P9_21, P9_22)

def stopEverythingAndQuit():
  stopEverything()
  import sys
  sys.exit(0)

def _getPwmPinDirectory(header, pin):
  hits = glob("/sys/devices/ocp.?/pwm_test_P%s_%s.*/" % (header, pin))
  if hits:
    return hits[0]
  else:
    log.fatal("Requested pin P%s_%s not found, double check that the firmware loaded..." % (header, pin))
    from pwm_utilities import stopEverythingAndQuit
    stopEverythingAndQuit()

def getTwin(pinName):
  if "P8_13" in pinName:
    return P8_19
  if "P8_19" in pinName:
    return P8_13
  if "P9_14" in pinName:
    return BLUE_LED
  if "P9_16" in pinName:
    return GREEN_LED
  if "P9_21" in pinName:
    return P9_22
  if "P9_22" in pinName:
    return P9_21
  log.error("Unrecognized pin: " + pinName)

def getPinFromShortName(shortName):
  if shortName in GREEN_LED:
    return GREEN_LED
  if shortName in BLUE_LED:
    return BLUE_LED
  if shortName in P8_13:
    return P8_13
  if shortName in P8_19:
    return P8_19
  if shortName in P9_21:
    return P9_21
  if shortName in P9_22:
    return P9_22

PWM_PERIOD = readInt(os.path.join(_getPwmPinDirectory(9, 21), "period"))
GREEN_LED = os.path.join(_getPwmPinDirectory(9, 14), "duty")
BLUE_LED = os.path.join(_getPwmPinDirectory(9, 16), "duty")
P8_13 = os.path.join(_getPwmPinDirectory(8, 13), "duty")
P8_19 = os.path.join(_getPwmPinDirectory(8, 19), "duty")
P9_21 = os.path.join(_getPwmPinDirectory(9, 21), "duty")
P9_22 = os.path.join(_getPwmPinDirectory(9, 22), "duty")

if __name__ == "__main__":
  stopEverything()
