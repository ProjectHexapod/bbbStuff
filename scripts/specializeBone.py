#!/usr/bin/env python
"""Beaglebone Specialization Script

Configures a flashed Beaglebone to be one of the six legs, three hips, or other computers.

Usage:
  ./specializeBone.py [options]

Options:
  -h, --help            Show this help screen.
  --version             Show the version.
  --leg=<leg>           Indicates which leg this BBB will be installed into (CW when viewed from above).
  --hip=<hip>           Indicates which hips this BBB will control (1=front, 3=rear).
  --console             Indicates that this BBB is the new console computer.
"""

import re
import subprocess

def changeHostname(name):
  subprocess.call(["hostnamectl", "set-hostname", name])

def changeIpAddress(ip):
  configuration = ""
  with open("/etc/systemd/network/eth0.network") as f:
    configuration = f.read()
  configuration = re.sub( "Address=\d+\.\d+\.\d+\.\d+(/\d+)?"
                        , "Address=" + ip
                        , configuration)
  with open("/etc/systemd/network/eth0.network", mode="w") as f:
    f.write(configuration)

def getIpForLeg(legNumber):
  return "10.1.1." + str(legNumber) + "/24"

def getIpForHip(hipNumber):
  return "10.1.1.1" + str(hipNumber) + "/24"

if __name__ == '__main__':
  from docopt import docopt
  args = docopt(__doc__, version="Bone Specializer v0.1")
  if args["--leg"]:
    changeHostname("leg" + args["--leg"])
    changeIpAddress(getIpForLeg(args["--leg"]))
    subprocess.call(["/home/stompy/bbbStuff/scripts/makeLegSymLinks.sh"])
  elif args["--hip"]:
    changeHostname("hip" + args["--hip"])
    changeIpAddress(getIpForHip(args["--hip"]))
    subprocess.call(["/home/stompy/bbbStuff/scripts/makeHipSymLinks.sh"])
  elif args["--console"]:
    changeHostname("centralcontrol")
    changeIpAddress("10.1.1.10/24")
    subprocess(["rm", "rf", "/mnt/hardware"])
