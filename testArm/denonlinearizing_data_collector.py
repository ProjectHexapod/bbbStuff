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
  --pwm=<pwm>                             Set the PWM pin.  P9_21.12 or P9_22.13  [default: P9_21.12]
  -f=<freq>, --frequency=<freq>           Set the feedback polling frequency in Hz.  [default: 100]
  -d=<duration>, --duration=<duration>    Set the duration of the run.  [default: 2]
  -r=<return>, --return=<return>          Set the return stroke duration.  [default: 2]
  -q, --quiet                             Supress printing the raw data.
  -s=<step>, --step=<step>                Sets the step size for the pulse sweep.  [default: 0]
"""

from pwm_utilities import *
import time
import utilities

def isInFirstNintyPercent(pwmName, reading):
  return "P9_21" in pwmName and reading < .9 or "P9_22" in pwmName and .1 < reading


def doSingleMotion(pulseWidth, pwmName, sampleFreq, runLength, loud=True):
  if loud:
    print "Pin Name, Pulse Width, Speed"
  initialTime = time.time()
  initialRead = utilities.readAin()
  sleepLen = 1. / sampleFreq
  prevTime = initialTime
  prevRead = initialRead
  now = prevTime
  reading = prevRead
  deadline = initialTime + runLength
  samples = 0

  writePwm(pwmName, pulseWidth)
  writePwm("P9_14.14", utilities.PWM_PERIOD - pulseWidth)  # LED
  while time.time() < deadline and isInFirstNintyPercent(pwmName, prevRead):
    samples += 1
    prevTime = now
    prevRead = reading
    time.sleep(sleepLen)
    now = time.time()
    reading = utilities.readAin()
    if loud:
      rate = (reading - prevRead) / (now - prevTime)
      print "%s, %s, %s" % (pwmName, pulseWidth, rate)
  stopEverything()

  elapsed = prevTime - initialTime
  return (prevRead - initialRead) / elapsed if elapsed > 0 else 0.

def doParameterSweep(stepSize, pwmName, sampleFreq, runLength, returnLength, loud=True):
  otherPwm = "P9_21.12" if pwmName == "P9_22.13" else "P9_22.13"
  results = []
  for width in range(utilities.PWM_PERIOD, utilities.PWM_PERIOD/5, -stepSize):
    writePwm(otherPwm, 1500000)
    writePwm("P9_16.15", 3500000)  # LED
    time.sleep(returnLength)
    stopEverything()
    dxdt = doSingleMotion(width, pwmName, sampleFreq, runLength, loud)
    results.append((width, dxdt))
  return results


if __name__ == "__main__":
  utilities.setupSignalHandlers()
  from docopt import docopt
  args = docopt(__doc__, version="Arm Calibration Script v0.1")
  step = int(args["--step"])
  pulseWidth = int(args["--pulse"])
  pwmPin = args["--pwm"]
  frequency = float(args["--frequency"])
  duration = float(args["--duration"])
  returnDuration = float(args["--return"])
  loud = "--quiet" not in args or not args["--quiet"]
  if step:
    print doParameterSweep(step, pwmPin, frequency, duration, returnDuration, loud)
  else:
    print doSingleMotion(pulseWidth, pwmPin, frequency, duration, loud)
  stopEverythingAndQuit()
