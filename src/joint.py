#!/usr/bin/env python
"""
"""

class Joint(object):
  def __init__( self
              , name
              , axis
              , centerOfRotationOffset
              , coordinateRotation = makeXYZRotationMatrix(0., 0., 0.)):
    self.axis = axis
    self.name = name
    self.centerOfRotationOffset = centerOfRotationOffset
    self.coordinateRotation = coordinateRotation
    self.parent = None
    self.child = None

  def setParent(self, parent):
    pass

  def setChild(self, child):
    pass


if __name__ == '__main__':
  pass
