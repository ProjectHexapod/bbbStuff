#!/usr/bin/env python
"""
"""

from glob import glob
import logging
import os

log = logging.getLogger(__name__)

def readInt(filename, retryCount=3):
  # many retries due to a bug in the kernel ADC driver that causes errno 11s sometimes
  for _ in range(retryCount):
    try:
      with open(filename) as f:
        return int(f.read())
    except IOError as ioe:
      if ioe.errno == 11:  # errno 11 means temporarily broken, try again
        pass
      else:
        log.error("Failed to read from " + filename, ioe)
        return None

def clamp(limits, control):
  return min(limits[1], max(limits[0], control))

def getPercentageIntoRange(range, distance):
  return (distance - range[0]) / (range[1] - range[0])

def projectPointIntoRange(range, percentage):
  return percentage * (range[1] - range[0]) + range[0]

def setupSignalHandlers():
  import signal
  from pwm_utilities import stopEverythingAndQuit
  signal.signal(signal.SIGABRT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGINT, lambda a,b: stopEverythingAndQuit())
  signal.signal(signal.SIGQUIT, lambda a,b: stopEverythingAndQuit())

def safeRun(main):
  setupSignalHandlers()
  try:
    main()
  except Exception as e:
    # no matter what everything should stop, so catch everything
    log.error("Something's gone horribly wrong!", e)
  stopEverythingAndQuit()

if __name__ == "__main__":
  pass
