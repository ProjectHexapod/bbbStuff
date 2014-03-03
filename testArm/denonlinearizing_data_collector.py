#!/usr/bin/env python
"""Denonlinearizing Data Collector

The denonlinearizing data collector is intended to collect data so that the
non-linear PWM -> Flow -> Motion function can be characterized and accounted for.

Usage:
  ./denonlinearizing_data_collector.py [options]

Options:
  -h, --help                              Show this help screen.
  --version                               Show the version information.
  -p=<pulse>, --pulse=<pul                Set the pulse width to sample.  [default: 4000000]
  --pwm=<pwm>                             Set the PWM pin.  P8_13, P8_19, P9_21 or P9_22  [default: P9_21]
  -f=<freq>, --frequency=<freq>           Set the feedback polling frequency in Hz.  [default: 100]
  -d=<duration>, --duration=<duration>    Set the duration of the run.  [default: 2]
  -r=<return>, --return=<return>          Set the return stroke duration.  [default: 2]
  -q, --quiet                             Supress printing the raw data.
  -s=<step>, --step=<step>                Sets the step size for the pulse sweep.  [default: 0]
"""

from adc_utilities import *
from pwm_utilities import *
import time

def isInFirstNintyPercent(pwmName, reading):
  return "P9_21" in pwmName and reading < .9 or "P9_22" in pwmName and .1 < reading


def doSingleMotion(pulseWidth, pwmName, sampleFreq, runLength, loud=True):
  if loud:
    print "Pin Name, Pulse Width, Speed"
  initialTime = time.time()
  initialRead = readAin(AIN3, ELBOW_RANGE)
  sleepLen = 1. / sampleFreq
  prevTime = initialTime
  prevRead = initialRead
  now = prevTime
  reading = prevRead
  deadline = initialTime + runLength
  samples = 0

  writePwm(pwmName, pulseWidth)
  writePwm(GREEN_LED, PWM_PERIOD - pulseWidth)
  while time.time() < deadline and isInFirstNintyPercent(pwmName, prevRead):
    samples += 1
    prevTime = now
    prevRead = reading
    time.sleep(sleepLen)
    now = time.time()
    reading = readAin(AIN3, ELBOW_RANGE)
    if loud:
      rate = (reading - prevRead) / (now - prevTime)
      print "%s, %s, %s" % (pwmName, pulseWidth, rate)
  stop(pwmName, GREEN_LED)

  elapsed = prevTime - initialTime
  return (prevRead - initialRead) / elapsed if elapsed > 0 else 0.

def doParameterSweep(stepSize, pwmName, sampleFreq, runLength, returnLength, loud=True):
  otherPwm = getTwin(pwmName)
  results = []
  for width in range(PWM_PERIOD, PWM_PERIOD/5, -stepSize):
    writePwm(otherPwm, 1500000)
    writePwm(BLUE_LED, 3500000)
    time.sleep(returnLength)
    stop(otherPwm, BLUE_LED)
    dxdt = doSingleMotion(width, pwmName, sampleFreq, runLength, loud)
    results.append((width, dxdt))
  return results


if __name__ == "__main__":
  import utilities
  utilities.setupSignalHandlers()
  from docopt import docopt
  args = docopt(__doc__, version="Arm Calibration Script v0.1")
  step = int(args["--step"])
  pulseWidth = int(args["--pulse"])
  pwmPin = getPinFromShortName(args["--pwm"])
  frequency = float(args["--frequency"])
  duration = float(args["--duration"])
  returnDuration = float(args["--return"])
  loud = "--quiet" not in args or not args["--quiet"]
  try:
    if step:
      print doParameterSweep(step, pwmPin, frequency, duration, returnDuration, loud)
    else:
      print doSingleMotion(pulseWidth, pwmPin, frequency, duration, loud)
  except:
    pass  # catch everything so that no matter what we stop the PWMs
  stopEverythingAndQuit()
