#!/usr/bin/env python
"""
"""

from pid import PIDController
from stop import stopEverything

def readInt(filename):
  with open(filename) as f:
    return int(f.read())

PWM_PERIOD = readInt("/sys/devices/ocp.3/pwm_test_P9_22.13/period")

def readAin():
  return readInt("/sys/bus/iio/devices/iio:device0/in_voltage3_raw")

def writePwm(name, val):
  with open("/sys/devices/ocp.3/pwm_test_%s/duty" % name, mode="w+") as f:
    f.write(val)

def clamp(control):
  return min(1., max(-1., control))

def mapControlToPwmPair(control):
  control = clamp(control)
  mag = 1. - abs(control)  # the 1 - here is because pwm duty 0 corresponds to full speed instead of stop
  result = mag * PWM_PERIOD * .8  + PWM_PERIOD * .2
  return (PWM_PERIOD, result) if control > 0 else (result, PWM_PERIOD)

def executePwmPair(pair):
  writePwm("P9_22.13", pair[0])
  writePwm("P9_21.12", pair[1])

def main():
  sensorRange = (1420, 3570)  # these values came from a run of calibrate.py
  pwmRange = (PWM_PERIOD/5, PWM_PERIOD)









if __name__ == "__main__":
  import signal
  signal.signal(signal.SIGINT, lambda a,b: stopEverything())
  main()
