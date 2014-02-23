#!/usr/bin/env python
"""Test Arm Calibrator

Usage:
  ./calibrate.py [options]

Options:
  -h, --help            Show this help screen.
  --version             Show the version.
  --ainroot=<ainroot>   The location of the AIN raw files.  [default: /sys/bus/iio/devices/iio:device0]
  --pwmroot=<pwmroot>   The location of the PWM control directories.  [default: /sys/devices/ocp.3]
"""

import os
import sys
import time

#  STATES
INIT = 0
EXTEND = 1
CONTRACT = 2
DONE = 3

state = INIT

def emptyRange():
  return (sys.maxint, -sys.maxint-1)  # not a typo, backwards so it will grow properly

def growRange(rng, val):
  return (min(rng[0], val), max(rng[1], val))

def readAin(root, pin):
  fn = os.path.join(root, "in_voltage%s_raw" % pin)
  with open(fn) as f:
    return int(f.read())

def main(args):
  ain3Range = emptyRange()
  aroot = args["--ainroot"]
  while state != DONE:
    a3 = readAin(aroot, 3)
    ain3Range = growRange(ain3Range, a3)
    stateDispatch()
    time.sleep(10)
  print ain3Range

def stateDispatch(proot):
  if state == INIT:
    startExtending(proot)
    state = EXTEND
  elif state == EXTEND:
    stop(proot)
    startContracting(proot)
    state = CONTRACT
  elif state == CONTRACT:
    stop(proot)
    state = DONE

def stop(proot):
  with open(os.path.join(proot, "pwm_test_P9_21.12")) as f:
    f.write("5000000")
  with open(os.path.join(proot, "pwm_test_P9_16.15")) as f:
    f.write("0")
  with open(os.path.join(proot, "pwm_test_P9_22.13")) as f:
    f.write("5000000")
  with open(os.path.join(proot, "pwm_test_P9_14.14")) as f:
    f.write("0")

def startExtending(proot):
  with open(os.path.join(proot, "pwm_test_P9_21.12")) as f:
    f.write("2500000")
  with open(os.path.join(proot, "pwm_test_P9_16.15")) as f:
    f.write("2500000")

def startContracting(proot):
  with open(os.path.join(proot, "pwm_test_P9_22.13")) as f:
    f.write("2500000")
  with open(os.path.join(proot, "pwm_test_P9_14.14")) as f:
    f.write("2500000")

if __name__ == "__main__":
  from docopt import docopt
  args = docopt(__doc__, version="Arm Calibration Script v0.1")
  main(args)
