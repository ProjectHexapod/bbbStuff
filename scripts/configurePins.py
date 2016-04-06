#!/usr/bin/env python
"""Cape of Stomping Pin Configurationist

Usage:
  ./configurePins.py [options]

Options:
  -h, --help            Show this help screen.
  --version             Show the version.
  --firmware=<firmware> The name of the device tree overlay.  [default: thigh_bone]
  --gpioroot=<gpioroot> The location of the GPIO control directories.  [default: /sys/class/gpio]
  --pwmperiod=<period>  The period of the PWM signal.  [default: 5000000]
  --pwmroot=<pwmroot>   The location of the PWM control directories.  [default: /sys/class/pwm]
"""
  # --ainroot=<ainroot>   The location of the AIN raw files.  [default: /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0]

import logging
import glob
import grp
import os
import pwd
import time

logging.info("Starting logger...")
log = logging.getLogger(__name__)

def firmwareLoaded(slots, firmwareName):
  log.debug("Checking for existing device tree overlay")
  with open(slots) as s:
    return firmwareName in s.read()

def loadFirmware(slots, firmwareName):
  log.info("Loading " + firmwareName + " overlay")
  with open(slots, "w") as s:
    s.write(firmwareName)

def pwmChipsAvailable(pwmroot):
  return (os.path.exists(os.path.join(pwmroot, "pwmchip0")) and
          os.path.exists(os.path.join(pwmroot, "pwmchip2")))

def pwmConfigured(pwmroot):
  # TODO: consider checking the period
  return (os.path.exists(os.path.join(pwmroot, "pwmchip0", "pwm0")) and
          os.path.exists(os.path.join(pwmroot, "pwmchip0", "pwm1")) and
          os.path.exists(os.path.join(pwmroot, "pwmchip2", "pwm0")) and
          os.path.exists(os.path.join(pwmroot, "pwmchip2", "pwm1")))

def configurePwm(pwmroot, period):
  configurePwmChip(pwmroot, "pwmchip0", period)
  configurePwmChip(pwmroot, "pwmchip2", period)
  with open("/sys/class/gpio/gpio27/value", "w") as f:
    f.write("1")
  # make the PWMs writeable
  chownFiles("/sys/devices/platform/ocp/*epwmss/*ehrpwm/pwm/pwmchip?/pwm?/duty_cycle")
    
def configurePwmChip(pwmroot, chip, period):
  if os.path.exists(os.path.join(pwmroot, chip)):
    configurePwmChannel(pwmroot, chip, "0", period)
    configurePwmChannel(pwmroot, chip, "1", period)
  else:
    log.error(chip + " is not present, is the device tree overlay loaded?")

def configurePwmChannel(pwmroot, chip, channelNo, period):
  with open(os.path.join(pwmroot, chip, "export"), "w") as f:
    f.write(channelNo)
  channel = "pwm" + channelNo
  with open(os.path.join(pwmroot, chip, channel, "period"), "w") as f:
    f.write(period)
  with open(os.path.join(pwmroot, chip, channel, "duty_cycle"), "w") as f:
    f.write("0")
  with open(os.path.join(pwmroot, chip, channel, "enable"), "w") as f:
    f.write("1")

def configureGpio(gpioroot, gpioNo, direction):
  if not os.path.exists(os.path.join(gpioroot, "gpio" + gpioNo)):
    with open(os.path.join(gpioroot, "export"), "w") as f:
      f.write(gpioNo)
  with open(os.path.join(gpioroot, "gpio" + gpioNo, "direction"), "w") as f:
    f.write(direction)

def chownFiles(nameGlob, user="stompy", group="stompy"):
  uid = pwd.getpwnam(user).pw_uid
  gid = grp.getgrnam(group).gr_gid
  for path in glob.glob(nameGlob):
    os.chown(path, uid, gid)

if __name__ == '__main__':
  from docopt import docopt
  args = docopt(__doc__, version="Pin Configurationist v0.1")

  slots = "/sys/devices/platform/bone_capemgr/slots"  # TODO: make this an arg
  firmware = args["--firmware"]
  if not firmwareLoaded(slots, firmware):
    loadFirmware(slots, firmware)

  pwmroot = args["--pwmroot"]
  # await the pwm chips (loading a device tree can take some milliseconds)
  overlayWaitTimerStart = time.time()
  while not pwmChipsAvailable(pwmroot) and time.time() - overlayWaitTimerStart < 2:
    time.sleep(0.1)

  gpioroot = args["--gpioroot"]

  # GPIO number is 32*chip number + offset 
  # e.g. P8_17 is on GPIO0_27: 32*0 + 27 = 27
  configureGpio(gpioroot, "26", "in")   # P8_14 # M2_statusflag
  configureGpio(gpioroot, "27", "out")  # P8_17 # enable pin
  configureGpio(gpioroot, "31", "in")   # P9_13 # M1_statusFlag
  configureGpio(gpioroot, "5", "in")    # P9_17 # DIP switch0
  configureGpio(gpioroot, "4", "in")    # P9_18 # DIP switch1
  configureGpio(gpioroot, "13", "in")   # P9_19 # DIP switch2
  configureGpio(gpioroot, "12", "in")   # P9_20 # DIP switch3
  configureGpio(gpioroot, "49", "in")   # P9_23 # DIP switch4
  configureGpio(gpioroot, "15", "in")   # P9_24 # DIP switch5
  # make the GPIOs writeable
  chownFiles("/sys/devices/platform/ocp/*gpio/gpio/gpio[0-9]*/value")

  if not pwmConfigured(pwmroot):
    configurePwm(pwmroot, args["--pwmperiod"])
