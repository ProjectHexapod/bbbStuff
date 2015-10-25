#!/usr/bin/env python
"""
"""

class PIDController(object):
  """Pretty basic PID controller, starting simple."""
  def __init__(self, kp, ki, kd):
    super(PIDController, self).__init__()
    self.kp = kp
    self.ki = ki
    self.kd = kd

    self.prev_error = 0
    self.i_accum = 0

  def update(self, target, current, dt):
    error = target - current
    d_error = (error - self.prev_error) / dt
    self.prev_error = error
    self.i_accum += self.ki * error * dt
    return self.kp * error + self.i_accum + self.kd * d_error


if __name__ == "__main__":
  from docopt import docopt
  arguments = docopt(__doc__, version='Stompy PID control. v0.1')
