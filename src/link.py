#!/usr/bin/env python
"""
"""

from math import cos, sin
import numpy as np

def makeMassMomentsMatrix(xx, xy, yy, xz, yz, zz):
  return np.array([[xx, xy, xz]
                 , [xy, yy, yz]
                 , [xz, yz, zz]])

def makeRotationMatrix(rx, ry, rz):  # these are euler angles in radians
  pass

class Link(object):
  def __init__( self
              , name
              , mass
              , massMoments
              , offset = np.array([0., 0., 0.])
              , rotation = makeRotationMatrix(0., 0., 0.)):
    self.name = name
    self.mass = mass
    self.massMoments = massMoments
    self.offset = offset
    self.rotation = rotation
    self.children = []
    self.parents = []




if __name__ == '__main__':
  pass
