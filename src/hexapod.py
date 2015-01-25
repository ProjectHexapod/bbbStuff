#!/usr/bin/env python
"""
"""

import makeMassMomentsMatrix as mmmm
from math import pi
import numpy as np


aboutY = np.array([0., 1., 0.])
aboutZ = np.array([0., 0., 1.])

# All magic numbers from Gui's "Simulation Export Drawings"
class Hexapod(object):
  def __init__(self):
    self.core = Link( "body"
                    , 1823.41  # kg
                    , mmmm( 499.7  # kgm^2
                          , 0.019, 3253.0
                          , -172.0, -0.096, 3049.0))
    hipSink = -0.495  # m
    endWidth = 0.5842
    midWidth = 0.6858
    front = 2.35117
    middle = .11597
    rear = -2.1192
    self.makeLeg(np.array([front, -endWidth, hipSink]), -pi/2.).setParent(self.core)
    self.makeLeg(np.array([middle, -midWidth, hipSink]), -pi/2.).setParent(self.core)
    self.makeLeg(np.array([rear, -endWidth, hipSink]), -pi/2.).setParent(self.core)
    self.makeLeg(np.array([rear, endWidth, hipSink]), pi/2.).setParent(self.core)
    self.makeLeg(np.array([middle, midWidth, hipSink]), pi/2.).setParent(self.core)
    self.makeLeg(np.array([front, endWidth, hipSink]), pi/2.).setParent(self.core)

  def makeLeg(self, hipCenterOfRotation, zRotation):
    yaw = Joint( "hipYaw"
               , aboutZ
               , hipCenterOfRotation
               , makeRotationMatrix(0., 0., zRotation))
    yaw.setChild(self.makeHip())
    return yaw

  def makeHip(self):
    hip = Link( "hip"
              , 28.231  # kg
              , mmmm( 0.337  #kgm^2
                    , 0., 0.327
                    , 0.026, 0., 0.417)
              , np.array([0.11156, 0., 0.006375]))  # m
    joint = Joint("hipPitch", aboutY, np.array([0.16784, 0., -0.04601]))  # m
    joint.setParent(hip)
    joint.setChild(self.makeThigh())
    return hip

  def makeThigh(self):
    thigh = Link( "thigh"
                , 64.053  # kg
                , mmmm( 1.334  #kgm^2
                      , 0., 10.92
                      , -0.34, 0., 10.62)
                , np.array([0.69035, 0., 0.12141]))  # m
    joint = Joint("kneePitch", aboutY, np.array([0.68125, 0., -0.12141]))  # m
    joint.setParent(thigh)
    joint.setChild(self.makeKnee())
    return thigh

  def makeKnee(self):
    knee = Link( "knee"
               , 39.145  # kg
               , mmmm( 0.775  # kgm^2
                     , 0., 5.636
                     , 1.148, 0., 5.471)
               , np.array([0.34127, 0., -0.00644]))  # m
    compliantZ = -0.09169
    top = Joint( "compliantTop"
               , aboutY
               , np.array([0.47153, 0., compliantZ])  # m
               , makeRotationMatrix(0., -pi/2., 0.))
    top.setParent(knee)
    top.setChild(self.makeCompliant())
    bottom = Joint( "compliantBottom"
                  , aboutY
                  , np.array([0.77633, 0., compliantZ])  # m
                  , makeRotationMatrix(0., -pi/2., 0.))
    bottom.setParent(knee)
    bottom.setChild(self.makeSterileCompliant())
    shinBot = Joint( "shinBottom"
                   , aboutY
                   , np.array([0.10013, 0., 0.])  # m
                   , makeRotationMatrix(0., pi/2., 0.))
    shinBot.setParent(knee.children[1].child)
    shinBot.setChild(knee.children[0].child.children[0].child)
    return knee

  def makeCompliant(self):
    comp = self.makeSterileCompliant()
    joint = Joint( "shinTop"
                 , aboutY
                 , np.array([0.10013, 0., 0.])  # m
                 , makeRotationMatrix(0., pi/2., 0.))
    joint.setParent(comp)
    joint.setChild(self.makeShin())
    return comp

  def makeSterileCompliant(self):
    return Link( "compliant"
               , 3.754  # kg
               , mmmm( 0.009  # kgm^2
                     , 0., 0.022
                     , 0., 0., 0.028)
               , np.array([0.10307, 0., 0.]))  # m

  def makeShin(self):
    shin = Link( "shin"
               , 18.983  # kg
               , mmmm( 0.145  # kgm^2
                     , 0., 1.859
                     , 0.243, 0., 1.827)
               , np.array([0.40805, 0., 0.00307]))  # m
    joint = Joint("ankleTop", aboutY, np.array([0.55536, 0., -0.09659])) # m
    joint.setParent(shin)
    joint.setChild(self.makeAnkle())
    return shin

  def makeAnkle(self):
    ankle = Link( "ankle"
                , 1.391  # kg
                , mmmm( 0.002  #kgm^2
                      , 0., 0.001
                      , 0., 0., 0.002)
                , np.array([0.01636, 0., 0.]))  # m
    joint = Joint("ankleBottom", aboutZ, np.array([0.02492, 0., 0.]))  # m
    joint.setParent(ankle)
    joint.setChild(self.makeFoot())
    return ankle

  def makeFoot(self):
    return Link( "foot"
               , 9.307  # kg
               , mmmm( 0.102  # kgm^2
                     , 0., 0.069
                     , 0., 0., 0.069)
               , np.array([0.11306, 0., 0.]))  # m

if __name__ == '__main__':
  pass
