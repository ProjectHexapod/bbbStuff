#!/usr/bin/env python
"""Closed Loop Test

Usage:
  ./closed_loop_test.py <setPoint>

Options:
  <setpoint>        Where should the dof go?  [default: 0.5]
"""

from adc_utilities import *
import logging
from pid import PIDController
from pwm_utilities import *
import time
from utilities import *

log = logging.getLogger(__name__)

def percentageClamp(control):
  return clamp((-1., 1.), control)

def mapControlToPwmPair(control):
  control = percentageClamp(control)
  mag = 1. - abs(control)  # the 1 - here is because pwm duty 0 corresponds to full speed instead of stop
  if mag > .99:  # put in a tiny deadband so that it's possible to stop if we're "close enough"
    return (PWM_PERIOD, PWM_PERIOD)
  result = int(projectPointIntoRange((1800000, 3400000), mag))
  return (PWM_PERIOD, result) if control > 0 else (result, PWM_PERIOD)

def executePwmPair(pair):
  log.debug("Commanding %s" % str(pair))
  writePwm(P9_22, pair[0])
  writePwm(P9_14, PWM_PERIOD - pair[0])  # LED
  writePwm(P9_21, pair[1])
  writePwm(P9_16, PWM_PERIOD - pair[1])  # LED



if __name__ == "__main__":
  from docopt import docopt
  args = docopt(__doc__, version="Closed Loop Control Test Script v0.1")
  setPoint = float(args["<setPoint>"])
  print setPoint

  def main():
    pid = PIDController(1., .001, .1)
    lastTime = time.time()
    while True:
      reading = readAin(AIN3, ELBOW_RANGE)
      log.debug("Read: %s" % reading)
      now = time.time()
      control = pid.update(setPoint, reading, now - lastTime)
      pair = mapControlToPwmPair(control)
      executePwmPair(pair)
      lastTime = now
      time.sleep(.1)  # because the valve response rate is 10Hz

  from utilties import safeRun
  safeRun(main)
