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

def getPercentageIntoRange(range, distance):
  return (distance - range[0]) / (range[1] - range[0])

def setupSignalHandlers():
  import signal
  from pwm_utilities import stopEverythingAndQuit
  signal.signal(signal.SIGABRT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGINT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGQUIT, lambda a,b: stopEverythingAndQuit())


if __name__ == "__main__":
  pass
