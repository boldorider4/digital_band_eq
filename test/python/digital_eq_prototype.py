from math import pi as Pi
from math import cos as Cos
from math import tan as Tan
import numpy as np

class digitalEq:

  def __init__(self, f_s):

    if f_s is None:
      print('invalid sampling frequency')
      return
    # input sampling frequency
    self.f_s = f_s
    # history of signal input and output
    self.x_n_1, self.x_n_2, self.y_n_1, self.y_n_2 = 0, 0, 0, 0
    # size of band filter bank
    self.eq_size = 0
    # filter parameters
    self.array_f_0 = None
    self.array_Q = None
    self.list_beta = []
    self.list_lambd = []
    self.list_alpha = []

  def init_eq(self, array_f_0, array_Q):

    if len(array_f_0) != len(array_Q):
      print('invalid eq bank size')
      return

    self.eq_size = len(array_f_0)
    self.array_f_0 = array_f_0
    self.array_Q = array_Q

    for f_0, Q in zip(array_f_0, array_Q):
      theta_0 = 2*Pi*(f_0/self.f_s)
      beta = .5 * ( 1 - Tan(.5*theta_0/Q) ) / ( 1 + Tan(.5*theta_0/Q) )
      self.list_beta.append(beta)
      self.list_lambd.append((.5 + beta) * Cos(theta_0))
      self.list_alpha.append((.5 - beta)/2)

    print("beta {}".format(self.list_beta))
    print("lambd {}".format(self.list_lambd))
    print("alpha {}".format(self.list_alpha))

  def process_sample(self, x_n):

    y_n = 0
    for beta, lambd, alpha in zip(self.list_beta, self.list_lambd, self.list_alpha):
      # y(n) = 2 { alpha*[x(n) - x(n-2)] + lambd*y(n-1) - beta*y(n-2) } / equalizer_size
      y_n += (2*alpha/self.eq_size)*x_n - (2*alpha/self.eq_size)*self.x_n_2 + \
             (2*lambd/self.eq_size)*self.y_n_1 - (2*beta/self.eq_size)*self.y_n_2
#      y_n += ( alpha*(x_n - self.x_n_2) + lambd*self.y_n_1 - beta*self.y_n_2 ) * (2/self.eq_size)

    # update input history
    self.x_n_2 = self.x_n_1
    self.x_n_1 = x_n
    self.y_n_2 = self.y_n_1
    self.y_n_1 = y_n

    return y_n
