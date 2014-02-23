#!/usr/bin/env python
"""
"""

def writePwm(name, val):
  with open("/sys/devices/ocp.3/pwm_test_%s/duty" % name, mode="w+") as f:
    f.write(str(val))

def stopEverything():
  writePwm("P9_21.12", 5000000)
  writePwm("P9_22.13", 5000000)
  writePwm("P9_14.14", 0)
  writePwm("P9_16.15", 0)

def stopEverythingAndQuit():
  stopEverything()
  import sys
  sys.exit(0)

if __name__ == "__main__":
  stopEverything()
