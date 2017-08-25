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
    self.array_f_0, self.array_Q = None, None
    self.array_beta, self.array_lambd, self.array_alpha = None, None, None


  def init_eq(self, array_f_0, array_Q):

    if len(array_f_0) != len(array_Q):
      print('invalid eq bank size')
      return

    self.eq_size = len(array_f_0)
    self.array_f_0 = np.array(array_f_0)
    self.array_Q = np.array(array_Q)
    self.y_n = np.zeros(self.eq_size)
    self.y_n_1 = np.zeros(self.eq_size)
    self.y_n_2 = np.zeros(self.eq_size)

    theta_0 = 2*np.pi*(self.array_f_0/self.f_s)
    self.array_beta = .5 * ( 1 - np.tan(.5*np.divide(theta_0,self.array_Q)) ) / \
                          ( 1 + np.tan(.5*np.divide(theta_0,self.array_Q)) )
    self.array_lambd = (.5 + self.array_beta) * np.cos(theta_0)
    self.array_alpha = (.5 - self.array_beta)/2


  def process_sample(self, x_n):

    self.y_n = 2 * (self.array_alpha*(x_n - self.x_n_2) + self.array_lambd*self.y_n_1 - \
                    self.array_beta*self.y_n_2) / self.eq_size

    # update input and output history
    self.x_n_2 = np.copy(self.x_n_1)
    self.x_n_1 = np.copy(x_n)
    self.y_n_2 = np.copy(self.y_n_1)
    self.y_n_1 = np.copy(self.y_n)

    return round(np.sum(self.y_n))