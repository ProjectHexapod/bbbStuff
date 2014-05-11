#!/usr/bin/env python
"""Closed Loop Test

Usage:
  ./closed_loop_test.py (-e <elbowSetPoint> [-s <shoulderSetPoint>]|--sin)

Options:
  --sin, --sine             Sine wave.
  -e <elbowSetPoint>        Where should the dof go?
  -s <shoulderSetPoint>     Where should the shoulder go?
"""

from adc_utilities import *
from arm_dynamics import getElbowPressure, getValveCommandFromControlSignal
import logging
import math
from pid import PIDController
from pwm_utilities import *
import time
from utilities import *

logging.basicConfig()
log = logging.getLogger(__name__)

def percentageClamp(control):
  return clamp((-1., 1.), control)

def mapControlToElbowPwmPair(control, pressure):
  control = percentageClamp(control)
  mag = 1. - abs(control)  # the 1 - here is because pwm duty 0 corresponds to full speed instead of stop
  if mag > .99:  # put in a tiny deadband so that it's possible to stop if we're "close enough"
    return (PWM_PERIOD, PWM_PERIOD)
  result = int(getValveCommandFromControlSignal(control, pressure))
  # result = int(projectPointIntoRange((1800000, 3400000), mag))
  return (PWM_PERIOD, result) if control > 0 else (result, PWM_PERIOD)

def mapControlToShoulderPwmPair(control):
  control = percentageClamp(control)
  mag = 1. - abs(control)  # the 1 - here is because pwm duty 0 corresponds to full speed instead of stop
  if mag > .99:  # put in a tiny deadband so that it's possible to stop if we're "close enough"
    return (PWM_PERIOD, PWM_PERIOD)
  result = int(projectPointIntoRange((3000000, 3650000), mag))
  return (PWM_PERIOD, result) if control > 0 else (result, PWM_PERIOD)

def executeElbowPwmPair(pair):
  log.debug("Commanding %s" % str(pair))
  writePwm(P9_21, pair[0])
  writePwm(GREEN_LED, PWM_PERIOD - pair[0])
  writePwm(P9_22, pair[1])
  writePwm(BLUE_LED, PWM_PERIOD - pair[1])

def executeShoulderPwmPair(pair):
  writePwm(P8_13, pair[0])
  writePwm(P8_19, pair[1])


if __name__ == "__main__":
  from docopt import docopt
  args = docopt(__doc__, version="Closed Loop Control Test Script v0.1")
  sinWave = "--sin" in args and args["--sin"]
  if not sinWave:
    elbowSetPoint = float(args["-e"])
    shoulderSetPoint = float(args["-s"])

  def main():
    elbowPid = PIDController(1., .001, .1)
    shoulderPid = PIDController(1., .001, .1)
    lastTime = time.time()
    while True:
      reading = readAin(AIN3, ELBOW_RANGE)
      log.debug("Read: %s" % reading)
      pistonPressure = getElbowPressure(reading)
      now = time.time()
      dt = now - lastTime
      elbowRate = 0
      # shoulderControl = 0
      if sinWave:
        elbowRate = elbowPid.update(math.sin(now)/2.+.5, reading, dt)
        # shoulderControl = shoulderPid.update(math.sin(now/3.)/8.+.85, reading, dt)
      else:
        elbowRate = elbowPid.update(elbowSetPoint, reading, dt)
        # shoulderControl = shoulderPid.update(shoulderSetPoint, reading, dt)
      elbowPair = mapControlToElbowPwmPair(elbowRate)
      # shoulderPair = mapControlToShoulderPwmPair(shoulderControl)
      executeElbowPwmPair(elbowPair)
      # executeShoulderPwmPair(shoulderPair)
      lastTime = now
      time.sleep(.1)  # because the valve response rate is 10Hz

  safeRun(main)
