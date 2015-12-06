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

def changeHostname(name):
  pass

def changeIpAddress(ip):
  pass

def disableNtpd():
  # TODO: write this once we get NTP going
  pass

if __name__ == '__main__':
  from docopt import docopt
  args = docopt(__doc__, version="Bone Specializer v0.1")
