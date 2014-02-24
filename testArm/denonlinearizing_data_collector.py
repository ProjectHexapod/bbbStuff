#!/usr/bin/env python
"""Denonlinearizing Data Collector

The denonlinearizing data collector is intended to collect data so that the
non-linear PWM -> Flow -> Motion function can be characterized and accounted for.

Usage:
  ./denonlinearizing_data_collector.py [options]

Options:
  -h, --help                             Show this help screen.
  --version                              Show the version information.
  -p=<pulse>, --pulse=<pulse>            Set the pulse width to sample.  [default: 4000000]
  --pwm=<pwm>                            Set the PWM pin.  P9_21.12 or P9_22.13  [default: P9_21.12]
  -f=<duration>, --frequency=<freq>      Set the feedback polling frequency in Hz.  [default: 100]
  -d=<duration>, --duration=<duration>   Set the duration of the run.  [default: 2]
  -s, --silent                           Supress printing the raw data.
"""

from stop import *
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

  return (prevRead - initialRead) / (prevTime - initialTime)



if __name__ == "__main__":
  utilities.setupSignalHandlers()
  from docopt import docopt
  args = docopt(__doc__, version="Arm Calibration Script v0.1")
  doSingleMotion(int(args["--pulse"])
                 , args["--pwm"]
                 , float(args["--frequency"])
                 , float(args["--duration"])
                 , "--silent" not in args or not args["--silent"])
  stopEverythingAndQuit()
