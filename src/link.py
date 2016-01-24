#!/usr/bin/env python
"""
"""

from math import cos, sin
import numpy as np

def makeMassMomentsMatrix(xx, xy, yy, xz, yz, zz):
  return np.array([[xx, xy, xz]
                 , [xy, yy, yz]
                 , [xz, yz, zz]])

def makeXYZRotationMatrix(rx, ry, rz):  # these are euler angles in radians
  RotX = np.array([[1,     0,          0      ] 
                 , [0, np.cos(rx), -np.sin(rx)] 
                 , [0, np.sin(rx),  np.cos(rx)]]))

  RotY = np.array([[np.cos(ry),  0,  np.sin(ry)] 
                 , [    0,       1,     0      ] 
                 , [-np.sin(ry), 0,  np.cos(ry)]]))

  RotZ = np.array([[ np.cos(rx), -np.sin(rx), 0] 
                 , [ np.sin(rx),  np.cos(rx), 0] 
                 , [    0,          0,        1]]))

  return RotZ*RotY*RotX


class Link(object):
  def __init__( self
              , name
              , mass
              , massMoments
              , offset = np.array([0., 0., 0.])
              , rotation = makeXYZRotationMatrix(0., 0., 0.)):
    self.name = name
    self.mass = mass
    self.massMoments = massMoments
    self.offset = offset
    self.rotation = rotation
    self.children = []
    self.parents = []




if __name__ == '__main__':
  pass
