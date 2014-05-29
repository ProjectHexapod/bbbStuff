#!/usr/bin/env python

import math

def getPercentageIntoRange(range, distance):
  return (distance - range[0]) / (range[1] - range[0])
getPercentageIntoRange((0,2), 1)
ELBOW_RANGE = (1420, 3570)  # these values came from a run of calibrate.py

aEdgeLen = 16.5   # inches
bEdgeLen = 4.375  # inches
readings = [(0.0037, 19.875, 1428)  # (percentage, inches, encoderRaw)
           , (0.4860, 17.125, 2465)
           , (0.9558, 14.25, 3475)]
inchesPerEncoder3 = (readings[2][1] - readings[0][1]) / (readings[2][0] - readings[0][0])
encoder3Bias = readings[2][1] - readings[2][0] * inchesPerEncoder3
lowerArmLength = 20.875  # inches
elbowBore = 2.
elbowRod = 1.25
elbowExtendArea = (elbowBore/2)**2 * math.pi
elbowRetractArea = elbowExtendArea - (elbowRod/2)**2 * math.pi
oilSpecificGravity = .87  # looked it up in Google
supplyPressure = 2000.



def getElbowPressureFromGravity(elbowReading, load = 100):
  a = aEdgeLen
  b = bEdgeLen
  c = elbowReading * inchesPerEncoder3 + encoder3Bias
  # law of cosines
  theta = math.acos((a**2 + b**2 - c**2) / (2*a*b))
  torque = load * lowerArmLength * math.sin(theta)
  force = torque / bEdgeLen
  if elbowReading < readings[1][0]:
    return (force / elbowExtendArea, -force / elbowRetractArea)
  else:
    return (-force / elbowExtendArea, force / elbowRetractArea)

def getValveCommandFromControlSignal(ctrl, pistonPressure):
  a1 = elbowRetractArea if ctrl > 0 else elbowExtendArea
  a2 = elbowExtendArea if ctrl > 0 else elbowRetractArea
  numer = (a2/a1)**2 + 1
  denom = supplyPressure - pistonPressure
  # ctrl * a1 is desired flow through the pressure side
  return ctrl * a1 * math.sqrt(oilSpecificGravity * numer / denom)





