#!/usr/bin/env python
"""
"""

class DegreeOfFreedom(object):
  def __init__(self, joint, bore, stroke, rod, minReading, maxReading, controller):
    super(DegreeOfFreedom, self).__init__()
    self.joint = joint
    self.bore = bore
    self.stroke = stroke
    self.rod = rod
    self.minReading = minReading
    self.maxReading = maxReading
    self.controller = controller
    

class DofController(object):
  def __init__(self, kp, ki, kd, maxSpeed, maxAccel, softstopPercentage):
    super(DofController, self).__init__()
    self.kp = kp
    self.ki = ki
    self.kd = kd
    self.maxSpeed = maxSpeed
    self.maxAccel = maxAccel
    self.softstopPercentage = softstopPercentage
    

if __name__ == '__main__':
  pass
