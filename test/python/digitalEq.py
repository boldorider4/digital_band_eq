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
    self.x_n_1, self.x_n_2, self.y_n, self.y_n_1, self.y_n_2 = 0, 0, None, None, None
    # size of band filter bank
    self.eq_size = 0
    # filter parameters
    self.array_f_0, self.array_Q, self.array_G = None, None, None
    self.array_beta, self.array_lambd, self.array_alpha = None, None, None


  def init_eq(self, array_f_0, array_Q, array_G):

    if len(array_f_0) != len(array_Q) or len(array_f_0) != len(array_G):
      print('invalid eq bank size')
      return -1

    self.eq_size = len(array_f_0)
    for f_0, Q, G in zip(array_f_0, array_Q, array_G):
      if f_0 > 20000 or f_0 < 20 or Q > 10 or Q < .1 or G > 1 or G < 0:
        print('invalid filter parameters')
        return -1

    self.array_f_0 = np.array(array_f_0)
    self.array_Q = np.array(array_Q)
    self.array_G = np.array(array_G)
    self.y_n = np.zeros(self.eq_size)
    self.y_n_1 = np.zeros(self.eq_size)
    self.y_n_2 = np.zeros(self.eq_size)

    theta_0 = 2*np.pi*(self.array_f_0/self.f_s)
    self.array_beta = .5 * ( 1 - np.tan(.5*np.divide(theta_0,self.array_Q)) ) / \
                          ( 1 + np.tan(.5*np.divide(theta_0,self.array_Q)) )
    self.array_lambd = (.5 + self.array_beta) * np.cos(theta_0)
    self.array_alpha = (.5 - self.array_beta)/2

    return 0


  def process_sample(self, x_n):

    self.y_n = 2 * (self.array_alpha*(x_n - self.x_n_2) + self.array_lambd*self.y_n_1 - \
                    self.array_beta*self.y_n_2) / self.eq_size

    # update input and output history
    self.x_n_2 = self.x_n_1
    self.x_n_1 = x_n
    self.y_n_2 = np.copy(self.y_n_1)
    self.y_n_1 = np.copy(self.y_n)

    return round(np.sum(self.array_G * self.y_n))
