#!/usr/bin/env python

import math

aEdgeLen = 16.5   # inches
bEdgeLen = 4.375  # inches
readings = [(1428, 19.875)  # (encoderRaw, inches)
           , (2465, 17.125)
           , (3475, 14.25)]
inchesPerEncoder3 = (readings[2][1] - readings[0][1]) / (readings[2][0] - readings[0][0])
encoder3Bias = 23.8  # inches
lowerArmLength = 20.875  # inches
elbowBore = 2.
elbowRod = 1.25
elbowExtendArea = (elbowBore/2)**2 * math.pi
elbowRetractArea = elbowExtendArea - (elbowRod/2)**2 * math.pi
oilSpecificGravity = .87  # looked it up in Google
supplyPressure = 2500.


def getElbowPressure(elbowReading, load = 200):  # PSI
  a = aEdgeLen
  b = bEdgeLen
  c = elbowReading * inchesPerEncoder3 + encoder3Bias
  # law of cosines
  theta = math.acos((a**2 + b**2 - c**2) / (2*a*b))
  torque = load * lowerArmLength * math.sin(theta)
  force = torque / bEdgeLen
  if elbowReading < readings[1][0]:
    return force / elbowExtendArea
  else:
    return force / elbowRetractArea

def getValveCommandFromControlSignal(ctrl, pistonPressure):
  a1 = elbowRetractArea if ctrl > 0 else elbowExtendArea
  a2 = elbowExtendArea if ctrl > 0 else elbowRetractArea
  numer = (a1/a2)**2 + 1
  denom = supplyPressure - pistonPressure
  # ctrl * a1 is desired flow through the pressure side
  return ctrl * a1 * math.sqrt(numer / denom)



# PID:: Set Point -> Position -> Desired Flow
# Physics:: Position -> Pressure
# ValveModel:: Pressure -> Desired Flow -> Command

# SG of AW 32  == .87  (from google)




